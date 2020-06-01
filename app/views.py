import json
import os

from slack import WebClient

from flask import request, Response

from app import app, db
from app.utils import check_signature
from app.models import Message


SLACK_OAUTH_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN', '')

client = WebClient(token=SLACK_OAUTH_TOKEN)


def get_elements(arr, type):
    return [a for a in arr if a['type'] == type]


def get_text(event):
    rt = get_elements(event['blocks'], 'rich_text')
    if rt:
        rts = get_elements(next(rt)['elements'], 'rich_text_section')
        if rts:
            text = next(get_elements(rts, 'elements', 'text'), default=None)
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
    return body


@app.route('/', methods=['POST'])
@check_signature
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


@app.route('/report', methods=['POST'])
@check_signature
def daily_report():
    messages = db.session.query(Message).filter_by(
        user=request.form['user_id'],
    )
    if messages.count() == 0:
        return Response('No messages found', status=200)
    message_list = []
    for m in messages:
        message_elements = m.message['blocks'][0]['elements'][0]['elements']
        message_elements.append({
            "type": "link",
            "url": "https://letsparty-workspace.slack.com/archives/{}/p{}".format(
                m.message['channel'],
                m.message['event_ts'].replace('.', '')
            ),
            "text": " Link "
        })
        message_list.append(
            {
                "type": "rich_text_section",
                "elements": message_elements
            }
        )
    response_message = {
            "blocks": [
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "elements": message_list,
                            "style": "bullet",
                            "indent": 0
                        },
                    ]
                }
            ]
        }
    return Response(
        json.dumps(response_message), status=200, headers={
            'Content-type': 'application/json'
        }
    )


@app.route('/clean-all', methods=['POST'])
@check_signature
def daily_clean_all():
    db.session.query(Message).filter_by(
        user=request.form['user_id'],
    ).delete()
    db.session.commit()
    return Response('Messages removed', status=200)
