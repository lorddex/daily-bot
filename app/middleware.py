import hashlib
import hmac
import json
import os

from flask import Request, Response

SLACK_SIGN_SECRET = os.environ.get('SLACK_SIGN_SECRET', '')


def hmac_sign(secret: str, message: str):
    signature = hmac.new(
            bytes(secret, "utf-8"), bytes(message, "utf-8"), digestmod=hashlib.sha256
        ).digest()

    return signature


class SlackSignCheckMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        sign = request.headers.get('x-slack-signature')
        body = json.dumps(request.get_json())
        self.app.logger.warning(sign)
        self.app.logger.warning(SLACK_SIGN_SECRET)
        self.app.logger.warning(body)
        calc_sign = hmac_sign(SLACK_SIGN_SECRET, body)
        self.app.logger.warning(calc_sign)
        if sign != calc_sign:
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
        return self.app(environ, start_response)
