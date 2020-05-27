from flask import request

from app import app, db
from app.models import Message


@app.route('/', methods=['POST'])
def challenge():
    if request.is_json:
        return request.get_json()['challenge']

def add_message():
    message = Message(user='a', message='b')
    db.session.add(message)
    db.session.commit()
    return 'Hello, world!'


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).last()
    return instance.user


