# app.py
# app.py
from quart import Quart, jsonify, request
import asyncio
from tasks import analyze_sentiment, analyze_metrics
from pymongo import MongoClient
from scrapper import InstagramScraper
import processor
from quart_cors import cors
import datetime

app = Quart(__name__)
# Enable CORS for all routes
app = cors(app, allow_origin="http://localhost:3000", allow_credentials=True)
# Set the timeout to 300 seconds (adjust as needed)
app.config['TIMEOUT'] = 360
# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db_name = 'rfs'
db = client[db_name]
scrapper = InstagramScraper(db_name)

# Function to set template structure for JSON responses


def set_response_template(status_code, message, percentage=0, is_done=False, data=None):
    return {
        'status': {'code': status_code, 'message': message},
        'progress': {'percentage': percentage, 'is_done': is_done},
        'data': data if data is not None else {}
    }

# Function to get task name based on endpoint


@app.route('/api/get_login_state', methods=['GET'])
async def get_login_state():
    data = client["main"]["users"].find_one({"username": db_name})
    data["_id"] = str(data["_id"])
    data.pop("scrap_acc", None)
    if ("is_logged" in data):
        return set_response_template(
            'SUCCESS', 'User Logged Status fetched', 100, True, data)


@app.route('/api/user_login', methods=['POST'])
async def user_login():
    try:
        data = await request.get_json()

        # Check if the required fields are present in the request
        if 'username' not in data or 'password' not in data:
            response_data = set_response_template(
                400, 'Missing required fields')
            return jsonify(response_data), 400

        username = data['username']
        password = data['password']
        # Your login logic here, using the received 'username' and 'password'
        scrapper.set_scrapper_acc(username, password)
        scrapper.login_user()

        if scrapper.is_connected:
            # Example response
            response_data = set_response_template(
                200, 'Login successful', data={'username': username})
            return jsonify(response_data)
        else:
            response_data = set_response_template(401, 'Login failed')
            return jsonify(response_data)
    except Exception as e:
        response_data = set_response_template(500, str(e))
        return jsonify(response_data), 500


def find_data(col_name: str, data, is_many=False):
    if (is_many):
        result = list(db[col_name].find(data))
        if result:
            for item in result:
                if item["_id"] is not None:
                    item["_id"] = str(item["_id"])
        return result
    else:
        result = db[col_name].find_one(data)
        if result["_id"] is not None:
            result["_id"] = str(result["_id"])
        return result


# Your routes
@app.route('/api/get_userinfo/<username>', methods=['GET'])
async def get_userinfo(username):
    # Your get_userinfo logic here
    result = find_data("users", {"username": username})
    response = set_response_template(
        'SUCCESS', 'User info retrieved successfully', 100, True, result)
    return jsonify(response)


@app.route('/api/get_user_posts/<username>', methods=['GET'])
async def get_user_posts(username):
    # Your get_user_posts logic here
    result = find_data("posts", {"username": username}, is_many=True)
    response = set_response_template(
        'SUCCESS', 'User posts retrieved successfully', 100, True, result)
    return jsonify(response)


@app.route('/api/get_post/<post_pk>', methods=['GET'])
def get_post(post_pk):
    # Your get_post logic here
    result = find_data("posts", {"post_pk": post_pk})
    response = set_response_template(
        'SUCCESS', 'Post retrieved successfully', 100, True, result)
    return jsonify(response)


@app.route('/api/get_users/', methods=['GET'])
def get_users():
    # Your get_post logic here
    result = find_data("users", {}, is_many=True)
    response = set_response_template(
        'SUCCESS', 'Post retrieved successfully', 100, True, result)
    return jsonify(response)


@app.route('/api/get_past_posts/<username>', methods=['POST'])
def get_past_posts(username):
    # Create a new document to monitor progress
    progress_doc = {'process': f'add_old_posts{username}',
                    'progress': 0, 'is_done': False}
    db['progress_collection'].insert_one(progress_doc)

    # Start the asynchronous task
    # asyncio.create_task(run_sync_user(username, progress_doc['_id']))
    scrapper.add_past_posts(username)
    result = find_data("users", {"username": username})

    response = set_response_template(
        'success', 'User add past posts done', 100, True, result)
    return jsonify(response)


@app.route('/api/get_past_comments/<post_pk>', methods=['POST'])
def get_past_comments(post_pk):
    try:
        # Create a new document to monitor progress
        # progress_doc = {'process': f'sync_post{post_pk}',
        #                 'progress': 0, 'is_done': False}
        # db['progress_collection'].insert_one(progress_doc)
        # Start the asynchronous task
        # asyncio.create_task(run_sync_post(post_pk, progress_doc['_id']))
        scrapper.add_past_comments(post_pk)
        result = find_data("posts", {"post_pk": post_pk})
        response = set_response_template(
            'success', 'User synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')

    return jsonify(response)


@app.route('/api/analyze_sentiment/<post_pk>', methods=['POST'])
async def analyze_sentiment_route(post_pk):
    try:
        # Create a new document to monitor progress
        progress_doc = {'process': f'analyze_sentiment{post_pk}{datetime.datetime.now()}',
                        'progress': 0, 'is_done': False}
        db['progress_collection'].insert_one(progress_doc)
        # Start the asynchronous task
        run_sync_sentiment(post_pk, progress_doc['_id'])
        result = find_data("posts", {"post_pk": post_pk})
        response = set_response_template(
            'success', 'User synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')
        return jsonify(response)


def run_sync_sentiment(post_pk, progress_id):
    try:
        post = find_data("posts", {"post_pk": post_pk})
        post.pop('_id')
        comments = post["comments"]
        total = len(comments)

        for i in range(0, total):
            if "sentiment" not in comments[i]:
                if (comments[i])["text"] is not None:
                    comments[i]["sentiment"] = processor.analyzeSentiment(
                        comments[i]["text"])
                    db['progress_collection'].update_one(
                        {'_id': progress_id}, {'$set': {'progress': (i+1)/total * 100, 'is_done': True}})

        # Update progress to 100 upon completion
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': 100, 'is_done': True}})
        db['posts'].update_one({"post_pk": post_pk}, {"$set": post})
    except Exception as e:
        # Handle errors and update progress accordingly
        print(str(e))
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': -1, 'is_done': True, "message": str(e)}})


@app.route('/api/analyze_metrics/<post_pk>', methods=['POST'])
async def analyze_metrics(post_pk):
    try:
        # Create a new document to monitor progress
        progress_doc = {'process': f'analyze_metrics{post_pk}',
                        'progress': 0, 'is_done': False}
        db['progress_collection'].insert_one(progress_doc)
        asyncio.create_task(run_sync_metrics(post_pk, progress_doc['_id']))
        result = find_data("posts", {"post_pk": post_pk})
        response = set_response_template(
            'success', 'User synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')
        return jsonify(response)


def run_sync_metrics(post_pk, progress_id):
    try:
        post_data = find_data("posts", {"post_pk": post_pk})
        post_data.pop("_id")
        user_data = find_data("users", {"username": post_data["username"]})
        views = post_data["view_count"]
        likes = post_data["likes_total"]
        comments = post_data['comments_total']
        date_today = datetime.datetime.now()
        followers = user_data["follower_count"]
        engagement_rate = (likes + comments + views) / followers
        metric = {
            'engagement_rate_score': engagement_rate,
            'datetime': date_today,
        }
        if ("engagement_rate" in post_data):
            engagement_arr = post_data["engagement_rate"]
        else:
            engagement_arr = []
        engagement_arr.append(metric)
        post_data["engagement_rate"] = engagement_arr
        # Update progress to 100 upon completion
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': 100, 'is_done': True}})
        db['posts'].update_one({"post_pk": post_pk}, {"$set": post_data})
    except Exception as e:
        # Handle errors and update progress accordingly
        print(str(e))
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': -1, 'is_done': True, "message": str(e)}})


@app.route('/api/sync_user/<username>', methods=['POST'])
async def sync_user(username):
    # Create a new document to monitor progress
    progress_doc = {'process': f'sync_user{username}',
                    'progress': 0, 'is_done': False}
    db['progress_collection'].insert_one(progress_doc)

    scrapper.sync_user(username)
    result = find_data("users", {"username": username})
    response = set_response_template(
        'SUCCESS', 'User synchronization started', 100, True, result)
    return jsonify(response)


@app.route('/api/sync_post/<post_pk>', methods=['POST'])
async def sync_post(post_pk):
    try:
        # Create a new document to monitor progress
        # progress_doc = {'process': f'sync_post{post_pk}',
        #                 'progress': 0, 'is_done': False}
        # db['progress_collection'].insert_one(progress_doc)
        scrapper.sync_post(post_pk)
        progress_doc = {'process': f'analyze_metrics{post_pk}',
                        'progress': 0, 'is_done': False}
        db['progress_collection'].insert_one(progress_doc)
        run_sync_metrics(post_pk, progress_doc['_id'])
        result = find_data("posts", {"post_pk": post_pk})
        client["main"]["users"].update_one(
            {"username": db_name}, {"$set": {"latest_sync": result["post_pk"]}})
        response = set_response_template(
            'success', 'Post synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
        print(e)
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')
        return jsonify(response)


async def run_sync_post(post_pk, progress_id):
    try:
        scrapper.sync_post(post_pk)
        # Update progress to 100 upon completion
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': 100, 'is_done': True}})
    except Exception as e:
        # Handle errors and update progress accordingly
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': -1, 'is_done': True}})


if __name__ == '__main__':
    try:
        print(client['main']["users"].find_one({"username": db_name}))
    except Exception as e:
        client['main']["users"].insert_one({
            "username": db_name,
            "password": "",
            "scrap_acc": {
                "username": "",
                "password": "",
                "session": None
            },
            "is_logged": False,
            "latest_sync": ""
        })
    app.run(debug=True)
