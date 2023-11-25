# tasks.py
from celery import Celery

celery = Celery(__name__, broker='pyamqp://guest@localhost//',
                backend='rpc://')


@celery.task
def analyze_sentiment(user_id):
    # Your sentiment analysis code here
    pass


@celery.task
def analyze_metrics(user_id):
    # Your metrics analysis code here
    pass
