import json
import os

from slack import WebClient
from slack.errors import SlackApiError

from flask import request, Response

from app import app, db
from app.models import Message

SLACK_VER_TOKEN = os.environ.get('SLACK_VER_TOKEN', '')
SLACK_OAUTH_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN', '')
SLACK_SIGN_SECRET = os.environ.get('SLACK_SIGN_SECRET', '')

client = WebClient(token=SLACK_OAUTH_TOKEN)


def handle_url_verification(message):
    return message['challenge']


def handle_app_mention(message):
    message = Message(user=message['user'], message=message['message'])
    db.session.add(message)
    db.session.commit()


def handle_message(event):
    message = Message(user=event['user'], message=event['text'])
    db.session.add(message)
    db.session.commit()

#    client.chat_postMessage(
#        channel='#test1',
#        text="Hello world!")


HANDLERS = {
    'event_callback': {
        'app_mention': handle_app_mention,
        'message': handle_message,
    },
    'url_verification': handle_url_verification,
}


def get_handler(event, handlers=HANDLERS):
    if handlers[event['type']]:
        handler = handlers[event['type']]
        if isinstance(handler, dict):
            return get_handler(event['event'], handlers=handler)
        return handler, event
    return None, None


def unwrap_event():
    body = request.get_json()
    app.logger.warning(json.dumps(body))
    return body


@app.route('/', methods=['POST'])
def message_received():
    if not request.is_json:
        return Response(status=204)

    event = unwrap_event()
    handler, event = get_handler(event)
    response = None
    status = 204
    if handler:
        response, status = handler(event)

    if response:
        return Response(response, status=status)
    return Response(status=status)


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).order_by(Message.id.desc()).first()
    return '{} {}'.format(instance.user, instance.message)
