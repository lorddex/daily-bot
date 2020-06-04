import json

from flask import request, Response

from app import app, db
from app.handlers import handle_message, handle_url_verification
from app.utils import check_signature
from app.models import Message


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
    return u'{} {}'.format(instance.user, instance.message)


@app.route('/report', methods=['POST'])
@check_signature
def daily_report():
    messages = db.session.query(Message).filter_by(
        user=request.form['user_id'],
    )

    if messages.count() == 0:
        return Response(u'No messages found', mimetype='text/plain', status=200)

    message_list = []
    for m in messages:
        message_elements = m.message['blocks'][0]['elements'][0]['elements']
        message_elements.append({
            'type': 'link',
            'url': 'https://{}.slack.com/archives/{}/p{}'.format(
                app.config['SLACK_WORKSPACE'],
                m.message['channel'],
                m.message['event_ts'].replace('.', '')
            ),
            'text': ' Link '
        })
        message_list.append(
            {
                'type': 'rich_text_section',
                'elements': message_elements
            }
        )
    response_message = {
            'blocks': [
                {
                    'type': 'rich_text',
                    'elements': [
                        {
                            'type': 'rich_text_list',
                            'elements': message_list,
                            'style': 'bullet',
                            'indent': 0
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
    return Response(u'Messages removed', mimetype='text/plain', status=200)
