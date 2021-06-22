"""API web service"""
from flask import Flask, jsonify
from api import api
from redis import Redis
from rq import Worker, Queue, Connection
from methods.connection import get_redis, await_job

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    return 'Hello World!'
