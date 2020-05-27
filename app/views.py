from flask import request

from app import app
from app.models import Message


@app.route('/add')
def hello_world_add():
    message = Message(user='a', message='b')
    message.save()
    return 'Hello, world!'


@app.route('/read')
def hello_world_read():
    message = Message()
    message.save()
    return 'Hello, world!'

