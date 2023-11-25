from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
import os
import pymongo
import datetime


class InstagramScraper:
    def __init__(self, db_name):
        self.logger = logging.getLogger()
        self.cl = Client()
        self.cl.delay_range = [1, 3]
        self.username = None
        self.password = None
        self.session = None
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_name = db_name
        self.set_attr_from_db()
        if (self.username != None and self.password != None):
            self.login_user_usejson()
        self.is_connected = False
        self.mydb = self.myclient[db_name]
        self.col_users = self.mydb["users"]
        self.col_posts = self.mydb["posts"]

    def set_scrapper_acc(self, username: str, password: str):
        self.username = username
        self.password = password

    def set_attr_from_db(self):
        user = self.myclient["main"]["users"].find_one(
            {"username": self.db_name})
        self.username = user["scrap_acc"]["username"]
        self.password = user["scrap_acc"]["password"]
        self.session = user["scrap_acc"]["session"]

    def login_user_usejson(self):
        session = self.session
        login_via_session = False
        login_via_pw = False
        if session:
            try:
                self.cl.set_settings(session)
                self.cl.login(self.username, self.password)

                # check if session is valid
                try:
                    self.cl.get_timeline_feed()
                except LoginRequired:
                    self.logger.info(
                        "Session is invalid, need to login via username and password")

                    old_session = self.cl.get_settings()

                    # use the same device uuids across logins
                    self.cl.set_settings({})
                    self.cl.set_uuids(old_session["uuids"])
                    self.cl.login(self.username, self.password)
                    new_session = self.cl.get_settings()
                    self.myclient["main"]["users"].update_one(
                        {"username": self.db_name}, {"$set": {"scrap_acc.session": new_session}})
                    self.is_connected = True
                login_via_session = True
                new_session = self.cl.get_settings()
                self.myclient["main"]["users"].update_one(
                    {"username": self.db_name}, {"$set": {"scrap_acc.session": new_session}})
                self.is_connected = True
                print("revalidate session")
            except Exception as e:
                self.logger.info(
                    "Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                self.logger.info(
                    "Attempting to login via username and password. username: %s" % self.username)
                if self.cl.login(self.username, self.password):
                    login_via_pw = True
                    new_session = self.cl.get_settings()
                    self.myclient["main"]["users"].update_one(
                        {"username": self.db_name}, {"$set": {"scrap_acc.session": new_session}})
                    self.is_connected = True
                    print("new session added")
            except Exception as e:
                self.logger.info(
                    "Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception(
                "Couldn't login user with either password or session")

    def get_userinfo(self, username: str):
        user_id = self.cl.user_id_from_username(username)
        user_info = self.cl.user_info(user_id)
        user_info_dict = {
            "user_pk": user_info.pk,
            "username": user_info.username,
            "full_name": user_info.full_name,
            "media_count": user_info.media_count,
            "follower_count": user_info.follower_count,
            "pfp_url": user_info.profile_pic_url,
            "posts": [],
            "end_cursor": None,
            "last_sync": datetime.datetime.now()
        }
        return user_info_dict

    def get_posts(self, target_user: str, amount: int):
        user_id = self.cl.user_id_from_username(target_user)
        medias = self.cl.user_medias(user_id, amount)
        posts = []
        for media in medias:
            posts.append({
                "username": media.user.username,
                "link": media.code,
                "post_pk": media.pk,
                "caption": media.caption_text,
                "comment_disabled": media.commenting_disabled_for_viewer,
                "comments_total": media.comment_count,
                "likes_total": media.like_count,
                "media_type": media.media_type,
                "product_type": media.product_type,
                "thumbnail_url": media.thumbnail_url,
                "view_count": media.view_count,
                "video_url": media.video_url,
                "comments": [],
                "last_sync": datetime.datetime.now()
            })
        return posts

    def get_posts_paginated(self, target_user: str, end_cursor: str | None):
        user_id = self.cl.user_id_from_username(target_user)
        medias, end_cursor = self.cl.user_medias_paginated(
            user_id, 100, end_cursor)
        posts = []
        for media in medias:
            posts.append({
                "username": media.user.username,
                "link": media.code,
                "post_pk": media.pk,
                "caption": media.caption_text,
                "comment_disabled": media.commenting_disabled_for_viewer,
                "comments_total": media.comment_count,
                "likes_total": media.like_count,
                "media_type": media.media_type,
                "product_type": media.product_type,
                "thumbnail_url": media.thumbnail_url,
                "view_count": media.view_count,
                "video_url": media.video_url,
                "comments": [],
                "end_cursor": None,
                "last_sync": datetime.datetime.now()
            })
        return posts, end_cursor

    def get_post(self, post_pk: str):
        post = self.cl.media_info(post_pk)
        post_dict = {
            "username": post.user.username,
            "link": post.code,
            "post_pk": post.pk,
            "caption": post.caption_text,
            "comment_disabled": post.commenting_disabled_for_viewer,
            "comments_total": post.comment_count,
            "likes_total": post.like_count,
            "media_type": post.media_type,
            "product_type": post.product_type,
            "thumbnail_url": post.thumbnail_url,
            "view_count": post.view_count,
            "video_url": post.video_url,
            "comments": [],
            "end_cursor": None,
            "last_sync": datetime.datetime.now()
        }
        return post_dict

    def get_post_comments(self, post_pk: str, amount: int):
        comments = self.cl.media_comments(post_pk, amount)
        comments_dict = []
        for comment in comments:
            comments_dict.append({
                "comment_pk": comment.pk,
                "username": comment.user.username,
                "text": comment.text
            })
        return comments_dict

    def get_post_comments_paginated(self, post_pk: str, end_cursor: str | None):
        comments, new_end_cursor = self.cl.media_comments_chunk(
            post_pk, 100, end_cursor)
        comments_dict = []
        for comment in comments:
            comments_dict.append({
                "comment_pk": comment.pk,
                "username": comment.user.username,
                "text": comment.text
            })
        return comments_dict, new_end_cursor

    def export_json(self, filename, json_target):
        file_path_user = filename + ".json"
        with open(file_path_user, 'w') as json_file:
            json.dump(json_target, json_file, indent=4)

    def export_userinfo_json(self, username_target, json_target):
        file_path_user = username_target + "_user_info" + ".json"

        # Check if the file already exists
        if os.path.exists(file_path_user):
            # Read the existing JSON data from the file
            with open(file_path_user, 'r') as existing_file:
                existing_data = json.load(existing_file)

            # Update the "posts" field with new data
            existing_data["posts"] += json_target.get("posts", [])

            # Write the updated data back to the file
            with open(file_path_user, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
        else:
            # If the file doesn't exist, create a new one
            with open(file_path_user, 'w') as json_file:
                json.dump(json_target, json_file, indent=4)

    def sync_post(self, post_pk: str):
        # Search for an existing document with the given username
        existing_post = self.col_posts.find_one({"post_pk": post_pk})
        new_post = self.get_post(post_pk)
        if existing_post["comments"]:
            comments_to_sync = new_post["comments_total"] - \
                existing_post["comments_total"]
            if (comments_to_sync > 0):
                new_comments = self.get_post_comments(
                    post_pk, comments_to_sync)
                new_post["comments"] = new_comments + existing_post["comments"]
            else:
                new_post["comments"] = existing_post["comments"]
            self.col_posts.update_one(
                {"post_pk": post_pk}, {"$set": new_post})
        else:
            self.add_past_comments(post_pk)

    def add_past_comments(self, post_pk: str):
        # Search for an existing document with the given username
        existing_post = self.col_posts.find_one({"post_pk": post_pk})
        new_post = self.get_post(post_pk)
        if existing_post["comments"]:
            if existing_post["end_cursor"]:
                new_comments, new_post["end_cursor"] = self.get_post_comments_paginated(
                    post_pk, existing_post["end_cursor"])
                new_post["comments"] = existing_post["comments"] + new_comments
            else:
                new_post["comments"] = existing_post["comments"]

        else:
            new_post["comments"], new_post["end_cursor"] = self.get_post_comments_paginated(
                post_pk, None)
        self.col_posts.update_one({"post_pk": post_pk}, {"$set": new_post})

    def sync_user(self, username: str):
        # Search for an existing document with the given username
        try:
            existing_user = self.col_users.find_one({"username": username})
            new_userinfo = self.get_userinfo(username)
            if existing_user:
                new_userinfo["posts"] = existing_user["posts"].copy()
                posts_to_sync = new_userinfo["media_count"] - \
                    existing_user["media_count"]
                if (posts_to_sync > 0):
                    new_posts = self.get_posts(username, posts_to_sync)
                    new_posts.reverse()
                    for post in new_posts:
                        new_userinfo["posts"].insert(0, post["post_pk"])
                    self.col_posts.insert_many(new_posts)
                self.col_users.update_one(
                    {"username": username},
                    {"$set": new_userinfo})
            else:
                posts, new_userinfo["end_cursor"] = self.get_posts_paginated(
                    username, new_userinfo["end_cursor"])
                posts_ids = []
                for post in posts:
                    posts_ids.append(post["post_pk"])
                new_userinfo["posts"] = posts_ids
                self.col_users.insert_one(new_userinfo)
                posts.reverse()
                self.col_posts.insert_many(posts)
            return True
        except ValueError as e:
            return False, str(e)

    def add_past_posts(self, username: str):
        # Search for an existing document with the given username
        existing_user = self.col_users.find_one({"username": username})
        new_userinfo = self.get_userinfo(username)
        if existing_user:
            if existing_user["end_cursor"]:
                new_posts = self.get_posts_paginated(
                    username, existing_user["end_cursor"])
                for post in new_posts:
                    new_userinfo["posts"].append(post["post_pk"])
                self.col_posts.insert_many(new_posts)
            self.col_users.update_one(
                {"username": username},
                {"$set": new_userinfo})
            return "updated"
        else:
            posts, new_userinfo["end_cursor"] = self.get_posts_paginated(
                username)
            posts_ids = []
            for post in posts:
                posts_ids.append(post["post_pk"])
            new_userinfo["posts"] = posts_ids
            self.col_users.insert_one(new_userinfo)
            posts.reverse()
            self.col_posts.insert_many(posts)
            return "created"

    def scrape_and_save(self, username: str):
        # self.sync_user(username)
        self.add_past_comments("3219994390684697487")
