import hashlib
import hmac
import os
import datetime

from flask import Request, Response

SLACK_SIGN_SECRET = os.environ.get('SLACK_SIGN_SECRET', '')
SLACK_SIGN_VERSION = 'v0'


def hmac_sign(secret: str, message: str):
    signature = hmac.new(
        bytes(secret, "utf-8"), bytes(message, "utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    return SLACK_SIGN_VERSION + '=' + signature


class SlackSignCheckMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        sign = request.headers.get('X-Slack-Signature')
        body = request.get_data().decode("utf-8")

        now = datetime.datetime.now()
        #if now.timestamp() - timestamp > 60 * 5:
        #    return

        to_sign = SLACK_SIGN_VERSION + ':' + timestamp + ':' + body
        calc_sign = hmac_sign(SLACK_SIGN_SECRET, to_sign)

        if sign != calc_sign:
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)

        self.app.logger.warning('OK')
        return self.app(environ, start_response)
