"""Parer api"""
# not implemented yet
from flask import Blueprint
from flask import jsonify, request
from rq import Queue
from methods.connection import get_redis, await_job
import time

api = Blueprint('api', __name__, url_prefix="api")
r = get_redis()

def format_comm(i):
    return {
        "id": str(i[0]),
        "video_id": str(i[1]),
        "channel_id": str(i[2]),
        "author_name": str(i[3]),
        "author_channel_id": str(i[4]),
        "text": str(i[5]),
        "likes": str(i[6]),
        "replies": str(i[7]),
        "view_rating": str(i[8]),
        "published_at": str(i[9]),
        "time": str(i[10])
    }

def format_vid(i):
    return {
        "id": str(i[0]),
        "title": str(i[1]),
        "views": str(i[2]),
        "likes": str(i[3]),
        "dislikes": str(i[4]),
        "comments": str(i[5]),
        "description": str(i[6]),
        "channel_id": str(i[7]),
        "duration": str(i[8]),
        "published_at": str(i[9]),
        "tags": str(i[10]),
        "default_language": str(i[11]),
        "made_for_kids": str(i[11])
    }

def format_chan(i):
    return {
        "id": str(i[0]),
        "title": str(i[1]),
        "description": str(i[2]),
        "custom_url": str(i[3]),
        "published_at": str(i[4]),
        "default_language": str(i[5]),
        "views": str(i[6]),
        "subscribers": str(i[7]),
        "hidden_subscribers": str(i[8]),
        "videos": str(i[9]),
        "keywords": str(i[10]),
        "country": str(i[11])
    }



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


# VIDEO/S
@api.route('/video', methods=['GET'])
def video_g():
    try:
        column = request.args.get('column')
        value = request.args.get('value')
        q = Queue('get_videos', connection=r)
        job = q.enqueue('get_videos.get_videos', "WHERE", column, value)
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_vid(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})


@api.route('/video', methods=['POST'])
def video_p():
    try:
        content = request.json
        content = list(dict(content).values())
        result = False
        for i in range(4):
            q = Queue('get_videos', connection=r)
            job = q.enqueue('get_videos.get_videos', "WHERE", 'id', content[0])
            await_job(job)
            result = job.result
            if result is not False:
                break
            time.sleep(5)
        vid_type = "upd" if result != () else "new"
        job = None
        if result is not False:
            q = Queue('parse_video', connection=r)
            if vid_type == "new":
                q = Queue('write_videos', connection=r)
                job = q.enqueue('write_videos.write_videos', [content])
            else:
                q = Queue('update_videos', connection=r)
                job = q.enqueue('update_videos.update_videos', content)
        else:
            return jsonify({"error": "Failed getting info from database", "data": False})
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/video', methods=['DELETE'])
def video_d():
    try:
        return jsonify({"data": "Not implemented yet"})  # Do we need this???
        id = request.args.get('id')
        q = Queue('delete_video', connection=r)
        job = q.enqueue('delete_video.delete_video', id)
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/videos', methods=['GET'])
def videos_g():
    try:
        q = Queue('get_videos', connection=r)
        job = q.enqueue('get_videos.get_videos')
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_vid(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})


@api.route('/channel', methods=['GET'])
def channel_g():
    try:
        column = request.args.get('column')
        value = request.args.get('value')
        q = Queue('get_channels', connection=r)
        job = q.enqueue('get_channels.get_channels', "WHERE", column, value)
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_chan(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})


@api.route('/channel', methods=['POST'])
def channel_p():
    try:
        content = request.json
        content = list(dict(content).values())
        q = Queue('write_channels', connection=r)
        job = q.enqueue('write_channels.write_channels', [content])
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/channel', methods=['DELETE'])
def channel_d():
    try:
        return jsonify({"data": "Not implemented yet"})  # Do we need this???
        id = request.args.get('id')
        q = Queue('delete_video', connection=r)
        job = q.enqueue('delete_video.delete_video', id)
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/channels', methods=['GET'])
def channels_g():
    try:
        q = Queue('get_channels', connection=r)
        job = q.enqueue('get_channels.get_channels')
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_chan(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})


# COMMENT/S
@api.route('/comment', methods=['GET'])
def comment_g():
    try:
        column = request.args.get('column')
        value = request.args.get('value')
        q = Queue('get_comments', connection=r)
        job = q.enqueue('get_comments.get_comments', "WHERE", column, value)
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_comm(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})


@api.route('/comment', methods=['POST'])
def comment_p():
    try:
        content = request.json
        content = list(dict(content).values())
        q = Queue('write_comments', connection=r)
        job = q.enqueue('write_comments.write_comments', [content])
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/comment', methods=['DELETE'])
def comment_d():
    try:
        return jsonify({"data": "Not implemented yet"})  # Do we need this???
        id = request.args.get('id')
        q = Queue('delete_comment', connection=r)
        job = q.enqueue('delete_comment.delete_comment', id)
        await_job(job, 5)
        if not job.result:
            return {"data": False}
        else:
            return jsonify({"data": True})
    except Exception as e:
        return jsonify({"error": e, "data": False})


@api.route('/comments', methods=['GET'])
def comments_g():
    try:
        q = Queue('get_comments', connection=r)
        job = q.enqueue('get_comments.get_comments')
        await_job(job, 5)
        if not job.result:
            return {"data": []}
        else:
            res = job.result
            data = {"data": []}
            for i in res:
                data["data"].append(format_comm(i))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e, "data": []})
