import json

from flask import Response
from slack import WebClient

from app import db, app
from app.models import Message


client = WebClient(token=app.config['SLACK_OAUTH_TOKEN'])


def handle_url_verification(message):
    return Response(message['challenge'], mimetype='text/plain', status=200)


def handle_message(event):
    # subtype messages are not supported
    if 'subtype' in event:
        return Response(status=204)
    message = Message(user=event['user'], message=event)
    db.session.add(message)
    db.session.commit()
    client.reactions_add(
        channel=event['channel'],
        name='thumbsup',
        timestamp=event['ts']
    )
    return Response(status=201)


def handle_interactive_message(event):
    '''
        Valid responses are:
        * delete
    '''
    if event['actions'][0]['value'] == 'delete':
        db.session.query(Message).filter_by(
            user=event['user']['id'],
        ).delete()
        db.session.commit()
    #return Response(json.dumps({}), status=200, headers={
    #        'Content-type': 'application/json',
    #    })
    return Response(status=200)


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
        'daily_0000_remove_messages': handle_interactive_message,
    }
}


def get_handler(key, event, handlers=HANDLERS):
    app.logger.warning(f'--- KEY: {key} --- {event}')
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
