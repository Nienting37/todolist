import flask
import datetime

from microblog import app, db
from flask import request
from microblog.models import User


def message(item):
    return flask.jsonify(
        {
            "id": item.id,
            "title": item.title,
            "should_alert": item.should_alert,
            "scheduled_time": item.scheduled_time,
            "done": item.done,
            "created_at": item.create_at,
            "updated_at": item.update_at
            }
    )


@app.route('/')
def homepage():
    return flask.jsonify('Hello, World!')


@app.route('/todo_list/', methods=['POST'])
def post_todo_list():
    param = request.get_json()
    if not param['title'] or not param['scheduled_time'] or not param['should_alert']:
        return flask.jsonify(f"缺少..."), 401
    todolist = User(title=param['title'], scheduled_time=param['scheduled_time'], should_alert=param['should_alert'])
    db.session.add(todolist)
    db.session.commit()
    return message(todolist)


@app.route('/todo_list/<int:todo_list_id>', methods=['GET'])
def todo_list_get(todo_list_id):
    item = User.query.filter_by(id=todo_list_id).first()
    if item is None:
        return flask.jsonify('Item not found.'), 404
    return message(item)


@app.route('/todo_list/<int:todo_list_id>', methods=['PUT'])
def todo_list_put(todo_list_id):
    param = request.get_json()
    if not param['title'] or not param['scheduled_time'] or not param['should_alert']:
        return flask.jsonify(f"缺少..."), 401
    item = User.query.filter_by(id=todo_list_id).first()
    if item is None:
        return flask.jsonify('Item not found.'), 404
    db.session.query(User).filter_by(id=todo_list_id).update(param)
    db.session.add(item)
    db.session.commit()
    return message(item)


@app.route('/todo_list/<int:todo_list_id>', methods=['DELETE'])
def todo_list_delete(todo_list_id):
    item = User.query.filter_by(id=todo_list_id).first()
    if item is None:
        return flask.jsonify('Item not found.'), 404
    db.session.delete(item)
    db.session.commit()
    return flask.jsonify({"result": True})


@app.route('/todo_list/<done_or_undone>/<int:todo_list_id>', methods=['PUT'])
def mark_done_or_undone(done_or_undone, todo_list_id):
    item = ""
    if done_or_undone == "mark_done":
        item = User.query.filter_by(id=todo_list_id).first()
        if item is None:
            return flask.jsonify('Item not found.'), 404
        item.done = True
    elif done_or_undone == "mark_undone":
        item = User.query.filter_by(id=todo_list_id).first()
        if item is None:
            return flask.jsonify('Item not found.'), 404
        item.done = False
    db.session.add(item)
    db.session.commit()
    return message(item)


@app.route('/todo_list/today', methods=['GET'])
def todo_list_today():
    day = str(datetime.date.today())
    return flask.jsonify([
        {
            "id": item.id,
            "title": item.title,
            "should_alert": item.should_alert,
            "scheduled_time": item.scheduled_time,
            "done": item.done,
            "created_at": item.create_at,
            "updated_at": item.update_at
        } for item in User.query.filter(User.scheduled_time.startswith(day)).all()
    ])


@app.route('/todo_list/all', methods=['GET'])
def todo_list_all():
    return flask.jsonify([
        {
            "id": item.id,
            "title": item.title,
            "should_alert": item.should_alert,
            "scheduled_time": item.scheduled_time,
            "done": item.done,
            "created_at": item.create_at,
            "updated_at": item.update_at
        } for item in User.query.all()
    ])


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
