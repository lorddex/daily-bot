from flask import Response
from slack import WebClient

from app import db, app
from app.models import Message


client = WebClient(token=app.config['SLACK_OAUTH_TOKEN'])


def handle_url_verification(message):
    return Response(message['challenge'], mimetype='text/plain', status=200)


def handle_message(event):
    message = Message(user=event['user'], message=event)
    db.session.add(message)
    db.session.commit()
    client.reactions_add(
        channel=event['channel'],
        name='thumbsup',
        timestamp=event['ts']
    )
    return Response(status=201)
