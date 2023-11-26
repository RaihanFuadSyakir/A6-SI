# app.py
# app.py
from quart import Quart, jsonify
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
scrapper = InstagramScraper("rfs")

# Function to set template structure for JSON responses


def set_response_template(status_code, message, percentage=0, is_done=False, data=None):
    return {
        'status': {'code': status_code, 'message': message},
        'progress': {'percentage': percentage, 'is_done': is_done},
        'data': data if data is not None else {}
    }

# Function to get task name based on endpoint


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
        asyncio.ensure_future(run_sync_sentiment(post_pk, progress_doc['_id']))
        result = find_data("posts", {"post_pk": post_pk})
        response = set_response_template(
            'success', 'User synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')
        return jsonify(response)


async def run_sync_sentiment(post_pk, progress_id):
    try:
        post = find_data("posts", {"post_pk": post_pk})
        post.pop('_id')
        comments = post["comments"]
        total = len(comments)

        for i in range(0, total):
            if "sentiment" not in comments[i]:
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
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': -1, 'is_done': True, "message": str(e)}})


@app.route('/api/analyze_metrics/<post_pk>')
def analyze_metrics_route(post_pk):
    try:
        # Create a new document to monitor progress
        progress_doc = {'process': f'analyze_metrics{post_pk}',
                        'progress': 0, 'is_done': False}
        db['progress_collection'].insert_one(progress_doc)

        # Start the asynchronous task
        asyncio.create_task(analyze_metrics(post_pk, progress_doc['_id']))

        response = set_response_template('success', 'User synchronization started', 0, False, {
            'progress_id': str(progress_doc['_id'])})
        return jsonify(response)
    except Exception as e:
        # Handle errors and update progress accordingly
        response = set_response_template('FAILURE', f'Error: {str(e)}')
        return jsonify(response)


async def analyze_metrics(post_pk, progress_id):
    try:
        # Update progress to 100 upon completion
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': 100, 'is_done': True}})
    except Exception as e:
        # Handle errors and update progress accordingly
        db['progress_collection'].update_one(
            {'_id': progress_id}, {'$set': {'progress': -1, 'is_done': True}})


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
        result = find_data("posts", {"post_pk": post_pk})
        response = set_response_template(
            'success', 'Post synchronization started', 100, True, result)
        return jsonify(response)
    except Exception as e:
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
    app.run(debug=True)
