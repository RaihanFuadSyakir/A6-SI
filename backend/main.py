# app.py
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from celery import Celery

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Analyzer'
app.config['JWT_SECRET_KEY'] = 'YlN7LGTytrK9OxXfpmZVorSm7ybu0lFJ'
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
celery = Celery(app.import_name,
                broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# ... (previous code)

# Protected endpoint to get user posts


@app.route('/ig_user_posts', methods=['GET'])
@jwt_required()
def ig_user_posts():
    current_user = get_jwt_identity()
    user = mongo.db.Users.find_one({'username': current_user})

    if user:
        # Assuming you have a field 'ig_user_id' in your Users collection
        ig_user_id = user.get('ig_user_id')
        if ig_user_id:
            # Your logic to fetch Instagram posts for the specified user ID
            # For now, just return a placeholder message
            return jsonify({'message': f'Posts for Instagram user {ig_user_id}'}), 200

    return jsonify({'message': 'User not found'}), 404

# Protected endpoint to trigger the heavy task


@app.route('/post_heavy_task', methods=['POST'])
@jwt_required()
def post_heavy_task():
    current_user = get_jwt_identity()
    user = mongo.db.Users.find_one({'username': current_user})

    if user:
        # Placeholder data for the heavy task (replace with actual data)
        user_info_dict = {'username': current_user, 'email': user.get('email')}
        posts = [{'title': 'Post 1', 'content': 'Content 1'},
                 {'title': 'Post 2', 'content': 'Content 2'}]

        # Trigger the heavy task asynchronously
        result = your_heavy_task.apply_async(args=(user_info_dict, posts))

        return jsonify({'task_id': result.id, 'status': 'Task started. Check later for the result.'}), 202

    return jsonify({'message': 'User not found'}), 404

# ... (previous code)


if __name__ == '__main__':
    app.run(debug=True)
