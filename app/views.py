import json

from flask import request, Response

from app import app, db
from app.handlers import get_handler
from app.utils import check_signature
from app.models import Message


@app.route('/', methods=['POST'])
@check_signature
def message_received():
    if not request.is_json:
        return Response(status=200)

    event = request.get_json()
    handler, event = get_handler(event['type'], event)

    if handler:
        response = handler(event)
    else:
        response = Response(status=204)

    return response


@app.route('/interactive', methods=['POST'])
@check_signature
def interactive_response_received():
    event = json.loads(request.form['payload'])
    handler, event = get_handler(event['type'], event)

    if handler:
        response = handler(event)
    else:
        response = Response(status=204)

    return response


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
                'elements': message_elements,
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
                            'indent': 0,
                        },
                    ],
                },
            ],
            'attachments': [
                {
                    'fallback': 'Would you like to remove the stored messages?',
                    'title': 'Would you like to remove the stored messages?',
                    'callback_id': 'daily_0000_remove_messages',
                    'color': '#3AA3E3',
                    'attachment_type': 'default',
                    'actions': [
                        {
                            'name': 'delete',
                            'text': 'Yes, delete them!',
                            'type': 'button',
                            'value': 'delete'
                        },
                        {
                            'name': 'no',
                            'text': 'No',
                            'type': 'button',
                            'value': 'no'
                        }
                    ]
                }
            ],
        }
    return Response(
        json.dumps(response_message), status=200, headers={
            'Content-type': 'application/json',
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
