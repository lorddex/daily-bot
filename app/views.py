from flask import request

from app import app, db
from app.models import Message


@app.route('/', methods=['POST'])
def add_message():
    if not request.is_json:
        return
    body = request.get_json()
    message = Message(user=body['user'], message=body['message'])
    db.session.add(message)
    db.session.commit()
    return ''


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).last()
    return '{} {}'.format(instance.user, instance.message)


