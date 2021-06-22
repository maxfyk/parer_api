"""Parer api"""
# not implemented yet
from flask import Blueprint
from flask import Flask, jsonify, request
from redis import Redis
from rq import Worker, Queue, Connection
from methods.connection import get_redis, await_job

api = Blueprint('api', __name__, url_prefix="api")
r = get_redis()


@api.route('/')
def index():
    return 'Hello World!'


# TASK/S
@api.route('/task', methods=['GET'])
def task_g():
    try:
        column = request.args.get('column')
        value = request.args.get('value')
        q = Queue('get_tasks', connection=r)
        job = q.enqueue('get_tasks.get_tasks', "WHERE", column, value)
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            return jsonify({"data": job.result})
    except Exception as e:
        return jsonify({"error": e, "data": []})


@api.route('/task', methods=['POST'])
def task_p():
    try:
        id = request.args.get('id')
        q = Queue('write_tasks', connection=r)
        job = q.enqueue('write_tasks.write_tasks', [id])
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/task', methods=['DELETE'])
def task_d():
    try:
        id = request.args.get('id')
        q = Queue('delete_task', connection=r)
        job = q.enqueue('delete_task.delete_task', id)
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/tasks', methods=['GET'])
def tasks_g():
    try:
        q = Queue('get_tasks', connection=r)
        job = q.enqueue('get_tasks.get_tasks')
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            return jsonify({"data": job.result})
    except Exception as e:
        return jsonify({"error": e, "data": []})
# TASK/S


@api.route('/video', methods=['GET'])
def video_g():
    return True


@api.route('/video', methods=['POST'])
def video_p():
    return True


@api.route('/video', methods=['DELETE'])
def video_d():
    return True


@api.route('/videos', methods=['GET'])
def videos_g():
    return True
