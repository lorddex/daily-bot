import json

from flask import request, Response

from app import app
from app.handlers import get_handler
from app.utils import check_signature


@app.route('/', methods=['POST'])
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
    handler, event = get_handler('daily-report', request.form)
    return handler(request.form)


@app.route('/clean-all', methods=['POST'])
@check_signature
def daily_clean_all():
    handler, event = get_handler('daily-clean-all', request.form)
    return handler(request.form)


@app.route('/add', methods=['POST'])
@check_signature
def daily_add():
    handler, event = get_handler('daily-add', request.form)
    return handler(request.form)
