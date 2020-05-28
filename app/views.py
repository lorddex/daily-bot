from flask import request, Response

from app import app, db
from app.models import Message


@app.route('/', methods=['POST'])
def add_message():
    if not request.is_json:
        return Response(status=204)
    body = request.get_json()
    message = Message(user=body['user'], message=body['message'])
    db.session.add(message)
    db.session.commit()
    return Response(status=204)


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).order_by(Message.id.desc()).first()
    return '{} {}'.format(instance.user, instance.message)


