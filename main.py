from microblog import app, db
from flask import request
from microblog.models import User
import datetime


@app.route('/')
def homepage():
    return 'Hello, World!'


@app.route('/todo_list/', methods=['POST'])
def post_todo_list():
    title = request.json['title']
    scheduled_time = request.json['scheduled_time']
    should_alert = request.json['should_alert']
    todolist = User(title=title, scheduled_time=scheduled_time, should_alert=should_alert)
    db.session.add(todolist)
    db.session.commit()
    return 'Post OK'


@app.route('/todo_list/<int:todo_list_id>', methods=['GET', 'PUT', 'DELETE'])
def todo_list(todo_list_id):
    if request.method == 'GET':
        item = User.query.filter_by(id=todo_list_id).first_or_404('Item not found.')
        print(item.id, item.title, item.scheduled_time, item.should_alert)
        return 'Get OK'

    elif request.method == 'PUT':
        param = request.get_json()
        item = User.query.filter_by(id=todo_list_id).first_or_404('Item not found.')
        db.session.query(User).filter_by(id=todo_list_id).update(param)
        db.session.add(item)
        db.session.commit()
        return 'Put OK'

    else:
        item = User.query.get(todo_list_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return 'Delete OK'
        else:
            return 'Item not found.'


@app.route('/todo_list/mark_done/<int:todo_list_id>', methods=['PUT'])
def mark_done(todo_list_id):
    item = User.query.filter_by(id=todo_list_id).first_or_404('Item not found.')
    item.done = True
    db.session.add(item)
    db.session.commit()
    return 'mark_done OK'


@app.route('/todo_list/mark_undone/<int:todo_list_id>', methods=['PUT'])
def mark_undone(todo_list_id):
    item = User.query.filter_by(id=todo_list_id).first_or_404('Item not found.')
    item.done = False
    db.session.add(item)
    db.session.commit()
    return 'mark_undone OK'


@app.route('/todo_list/today', methods=['GET'])
def todo_list_today():
    day = str(datetime.date.today())
    item = User.query.filter(User.scheduled_time.startswith(day)).all()
    if item:
        for i in range(len(item)):
            print(item[i].id, item[i].title, item[i].scheduled_time, item[i].should_alert, item[i].done,
                  item[i].create_at, item[i].update_at)
        return "today_list OK"
    else:
        return "No todo_list today"


@app.route('/todo_list/all', methods=['GET'])
def todo_list_all():
    all = User.query.all()
    if all:
        for i in range(len(all)):
            print(all[i].id, all[i].title, all[i].scheduled_time, all[i].should_alert, all[i].done,
                  all[i].create_at, all[i].update_at)
        return "all_list OK"
    else:
        return "No todo_list"


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
