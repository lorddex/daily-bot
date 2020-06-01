import hashlib
import hmac
import json
import os
import datetime

from flask import Request, Response

SLACK_SIGN_SECRET = os.environ.get('SLACK_SIGN_SECRET', '')


def hmac_sign(secret: str, message: str):
    signature = hmac.new(
        bytes(secret, "utf-8"), bytes(message, "utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    return 'v0=' + signature


class SlackSignCheckMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        now = datetime.datetime.now()
        #if now.timestamp() - timestamp > 60 * 5:
        #    return
        sign = request.headers.get('X-Slack-Signature')
        self.app.logger.warning(sign)
        to_sign = 'v0:' + timestamp + ':' + str(request.data)
        calc_sign = hmac_sign(SLACK_SIGN_SECRET, to_sign)
        self.app.logger.warning(calc_sign)
        if sign != calc_sign:
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
        return self.app(environ, start_response)
