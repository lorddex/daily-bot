from flask import request

from app import app, db
from app.models import Message


@app.route('/add')
def hello_world_add():
    message = Message(user='a', message='b')
    db.session.add(message)
    db.session.commit()
    return 'Hello, world!'


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).first()
    return instance.user

