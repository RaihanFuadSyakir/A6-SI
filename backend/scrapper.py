from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
import os
import pymongo


class InstagramScraper:
    def __init__(self, username, password, db_name):
        self.logger = logging.getLogger()
        self.cl = Client()
        self.cl.delay_range = [1, 3]
        self.username = username
        self.password = password
        self.login_user_usejson()
        self.db_name = db_name
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient[db_name]
        self.col_users = self.mydb["Users"]
        self.col_posts = self.mydb["Posts"]
        self.end_cursor_get_posts = None
        self.end_cursor_get_comments = None

    def login_user_usejson(self):
        session_file = "session.json"
        if os.path.exists(session_file):
            session = self.cl.load_settings(session_file)
        else:
            session = None

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
                login_via_session = True
            except Exception as e:
                self.logger.info(
                    "Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                self.logger.info(
                    "Attempting to login via username and password. username: %s" % self.username)
                if self.cl.login(self.username, self.password):
                    login_via_pw = True
                    self.cl.dump_settings("session.json")
            except Exception as e:
                self.logger.info(
                    "Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception(
                "Couldn't login user with either password or session")

    def get_userinfo(self, target_user):
        user_id = self.cl.user_id_from_username(target_user)
        user_info = self.cl.user_info(user_id)
        user_info_dict = {
            "user_pk": user_info.pk,
            "username": user_info.username,
            "full_name": user_info.full_name,
            "media_count": user_info.media_count,
            "follower_count": user_info.follower_count,
            "pfp_url": user_info.profile_pic_url,
            "posts": []
        }
        return user_info_dict

    def get_posts(self, target_user: str, amount: int) -> dict:
        user_id = self.cl.user_id_from_username(target_user)
        medias = self.cl.user_medias(user_id, amount)
        posts = []
        for media in medias:
            posts.append({
                "username": media.user.username,
                "link": media.code,
                "post_id": media.pk,
                "caption": media.caption_text,
                "comment_disabled": media.commenting_disabled_for_viewer,
                "comments_total": media.comment_count,
                "likes_total": media.like_count,
                "media_type": media.media_type,
                "product_type": media.product_type,
                "thumbnail_url": media.thumbnail_url,
                "view_count": media.view_count,
                "video_url": media.video_url,
                "comments": []
            })
        return posts

    def get_posts_paginated(self, target_user: str, amount: int, end_cursor):
        user_id = self.cl.user_id_from_username(target_user)
        medias, end_cursor = self.cl.user_medias_paginated(
            user_id, 5, end_cursor=end_cursor)
        posts = []
        for media in medias:
            posts.append({
                "username": media.user.username,
                "link": media.code,
                "post_id": media.pk,
                "caption": media.caption_text,
                "comment_disabled": media.commenting_disabled_for_viewer,
                "comments_total": media.comment_count,
                "likes_total": media.like_count,
                "media_type": media.media_type,
                "product_type": media.product_type,
                "thumbnail_url": media.thumbnail_url,
                "view_count": media.view_count,
                "video_url": media.video_url,
                "comments": []
            })
        return posts, end_cursor

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

    def scrape_and_save(self, target_user):
        userinfo = self.get_userinfo(target_user)
        # userinfo["posts"] = self.get_posts(target_user, 5)
        end_cursor = "QVFBVmt2bi1oX3duMTlGdWlXTldkQkZuVHdQN3JJTWRQXzlBZTYtQXRuLXIyOG5tMDk4NGczYUNLUzROZWNDZVF2T1JqeTVmMkNhX0Fyc1BhcWpQWm1FVw=="
        userinfo["posts"], end_cursor = self.get_posts_paginated(
            target_user, 5, end_cursor)
        print(end_cursor)
        # self.export_json(f'{target_user}_infoacc', userinfo)
        self.export_userinfo_json(target_user, userinfo)
        # self.col_users.insert_one(userinfo)


# Example usage:
scraper = InstagramScraper("meltfrosty", "stayfrosty", "user1")
print(scraper)
scraper.scrape_and_save("monsterhuntergame")
