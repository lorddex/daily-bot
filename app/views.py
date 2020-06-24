#  Daily-Bot
#  Copyright (C) 2020  Francesco Apollonio
#
#  This file is part of Daily-Bot.
#  Daily-Bot is free software:
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json

from flask import request, Response

from app import app
from app.handlers import get_handler
from app.utils import check_signature


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
    handler, event = get_handler('daily-report', request.form)
    return handler(request.form)


@app.route('/clean-all', methods=['POST'])
@check_signature
def daily_clean_all():
    handler, event = get_handler('daily-clean-all', request.form)
    return handler(request.form)
