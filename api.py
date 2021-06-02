"""Parer api"""
# not implemented yet
import sys
from flask import Blueprint
from redis import Redis
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor


api = Blueprint('urls2', __name__, url_prefix="api")
redis = get_redis()


@api.route('/')
def index():
    return 'api is not implemented yet'
