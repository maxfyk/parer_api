"""Parer api"""
# not implemented yet
import sys
from flask import Blueprint
from redis import Redis
from rq import Worker, Queue, Connection


def get_redis():
    """Returns redis connection"""
    try:
        redis = Redis(host='redis', port=6379)
    except Redis.DoesNotExist as error:
        print(error)
        sys.exit("Error: Faild connecting to redis")
    return redis


api = Blueprint('urls2', __name__, url_prefix="api")
redis = get_redis()


@api.route('/')
def index():
    return 'api is not implemented yet'
