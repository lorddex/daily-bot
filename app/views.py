import json
from flask import request, Response

from app import app, db
from app.models import Message


def handle_app_mention(message):
    message = Message(user=message['user'], message=message['message'])
    db.session.add(message)
    db.session.commit()


def handle_message(event):
    message = Message(user=event['user'], message=event['text'])
    db.session.add(message)
    db.session.commit()

HANDLERS = {
    'app_mention': handle_app_mention,
    'message': handle_message,
}


def unwrap_event():
    body = request.get_json()
    app.logger.warning(json.dumps(body))
    return body


@app.route('/', methods=['POST'])
def add_message():
    if not request.is_json:
        return Response(status=204)

    message = unwrap_event()
    event = message['event']
    if HANDLERS[event['type']]:
        HANDLERS[event['type']](event)

    return Response(status=204)


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).order_by(Message.id.desc()).first()
    return '{} {}'.format(instance.user, instance.message)


