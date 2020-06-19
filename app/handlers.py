import json
import requests

from flask import Response
from slack import WebClient

from app import db, app
from app.message_templates import (
    build_daily_report_message,
    build_bloc_section_plain_text,
    build_text,
    build_link,
)
from app.models import Message


client = WebClient(token=app.config['SLACK_OAUTH_TOKEN'])


def handle_url_verification(message):
    return Response(message['challenge'], mimetype='text/plain', status=200)


def _event_clean_up(event):
    """
    Removes the text/blocks from the message in order to not store these into our DB.
    """
    copy = event.copy()
    if 'text' in copy:
        copy['text'] = ''
    if 'blocks' in copy:
        copy['blocks'] = []
    return copy


def handle_message(event):
    # subtype messages are not supported
    if 'subtype' in event:
        return Response(status=204)
    message = Message(
        user=event['user'],
        channel=event['channel'],
        ts=event['ts'],
    )
    db.session.add(message)
    db.session.commit()
    client.reactions_add(
        channel=event['channel'],
        name='thumbsup',
        timestamp=event['ts']
    )
    return Response(status=201)


def handle_daily_add(event):
    message = Message(user=event['user_id'], message=[build_text(event['text'])])
    db.session.add(message)
    db.session.commit()
    return Response(
        json.dumps(build_bloc_section_plain_text(f'Message {event["text"]} added')),
        status=200,
        headers={
            'Content-type': 'application/json',
        }
    )


def handle_daily_report(event):
    messages = db.session.query(Message).filter_by(
        user=event['user_id'],
    ).order_by(Message.created)

    if messages.count() == 0:
        return Response(
            json.dumps(build_bloc_section_plain_text('No messages found')),
            status=200,
            headers={
                'Content-type': 'application/json',
            }
        )

    ms = []
    for m in messages:
        params = {
            'token': app.config['SLACK_OAUTH_TOKEN'],
            'channel': m.channel,
            'inclusive': True,
            'latest': m.ts,
            'limit': 1,
        }
        res = requests.get(
            'https://www.slack.com/api/conversations.history',
            params=params,
        )
        app.logger.warning('{} {}'.format(params, res.json()))
        message = res.json()
        message_elements = message['messages'][0]['blocks'][0]['elements'][0]['elements']
        message_elements.append(build_link('https://{}.slack.com/archives/{}/p{}'.format(
                app.config['SLACK_WORKSPACE'],
                m.channel,
                m.ts.replace('.', '')
        ), ' Link '))
        ms.append({'message': m, 'elements': message_elements})

    response_message = build_daily_report_message(ms)
    app.logger.warning(response_message)
    return Response(
        json.dumps(response_message),
        status=200,
        headers={
            'Content-type': 'application/json',
        }
    )


def handle_daily_clean_all(event):
    db.session.query(Message).filter_by(
        user=event['user_id'],
    ).delete()
    db.session.commit()
    return Response(u'Messages removed', mimetype='text/plain', status=200)


HANDLERS = {
    'event_callback': {
        'field': 'type',
        'extract_event': lambda e: e['event'],
        'app_mention': handle_message,
        'message': handle_message,
    },
    'url_verification': handle_url_verification,
    'interactive_message': {
        'field': 'callback_id',
    },
    'daily-report': handle_daily_report,
    'daily-clean-all': handle_daily_clean_all,
    'daily-add': handle_daily_add,
}


def get_handler(key, event, handlers=HANDLERS):
    if not isinstance(handlers, dict):
        return None, None

    if key not in handlers:
        return None, None

    handler = handlers[key]
    if isinstance(handler, dict):
        field = handler['field']
        if 'extract_event' in handler:
            event = handler['extract_event'](event)
        return get_handler(event[field], event, handlers=handler)
    return handler, event
