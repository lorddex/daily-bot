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


def get_elements(arr, type):
    return [a for a in arr if a['type'] == type]


def get_text(event):
    rt = get_elements(event['blocks'], 'rich_text')
    app.logger.warning(rt)
    if rt:
        rts = get_elements(next(rt)['elements'], 'rich_text_section')
        app.logger.warning(rts)
        if rts:
            text = next(get_elements(rts, 'elements', 'text'), default=None)
            app.logger.warning(text)
            return text
    return None


def handle_url_verification(message):
    return Response(message['challenge'], status=200)


def handle_message(event):
    message = Message(user=event['user'], message=event)
    db.session.add(message)
    db.session.commit()
    client.reactions_add(
        channel=event['channel'],
        name="thumbsup",
        timestamp=event['ts']
    )
    return Response(status=201)

#    client.chat_postMessage(
#        channel='#test1',
#        text="Hello world!")


HANDLERS = {
    'event_callback': {
        'app_mention': handle_message,
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
    response = Response(status=204)
    if handler:
        response = handler(event)

    return response


@app.route('/read')
def hello_world_read():
    instance = db.session.query(Message).order_by(Message.id.desc()).first()
    return '{} {}'.format(instance.user, instance.message)


@app.route('/daily-report', methods=['POST'])
def daily_report():
    messages = db.session.query(Message).filter_by(
        user='UHHPEMDDM',
    )
    return Response(
        json.dumps({
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Found {} messages".format(messages.count())
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Partly cloudy today and tomorrow"
                    }
                }
            ]
        }), status=200, headers={
            'Content-type': 'application/json'
        }
    )
