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

import functools
import hashlib
import hmac
import datetime
import json

import requests
from flask import Response, request

from app import app


def hmac_sign(secret: str, message: str) -> str:
    signature = hmac.new(
        bytes(secret, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256
    ).hexdigest()

    return app.config['SLACK_SIGN_VERSION'] + '=' + signature


def check_signature(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if app.config['SLACK_VERIFICATION_ENABLED']:
            return func(*args, **kwargs)

        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        sign = request.headers.get('X-Slack-Signature')
        body = request.get_data().decode('utf-8')

        if not timestamp or not sign or not body:
            return Response(u'Missing timestamp, sign or body', mimetype='text/plain', status=400)

        now = datetime.datetime.now()
        if now > datetime.datetime.fromtimestamp(float(timestamp)) + datetime.timedelta(0, 60*5):
            return Response(u'Expired signature', mimetype='text/plain', status=400)

        to_sign = app.config['SLACK_SIGN_VERSION'] + ':' + timestamp + ':' + body
        calc_sign = hmac_sign(app.config['SLACK_SIGN_SECRET'], to_sign)

        if not hmac.compare_digest(sign, calc_sign):
            return Response(u'Authorization failed', mimetype='text/plain', status=401)

        return func(*args, **kwargs)

    return wrapper


class GetSlackMessageException(Exception):
    pass


def get_slack_message(channel, ts):
    params = {
        'token': app.config['SLACK_OAUTH_TOKEN'],
        'channel': channel,
        'inclusive': True,
        'latest': ts,
        'limit': 1,
    }
    res = requests.get(
        'https://www.slack.com/api/conversations.history',
        params=params,
    )
    json_res = res.json()
    if not json_res['ok']:
        raise GetSlackMessageException(
            'Error while accessing the message: {}'.format(
                json.dumps(json_res['errors']),
            )
        )
    return res.json()['messages'][0]
