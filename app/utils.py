import functools
import hashlib
import hmac
import os
import datetime

from flask import Response, request

from app import app


def hmac_sign(secret: str, message: str) -> str:
    signature = hmac.new(
        bytes(secret, "utf-8"), bytes(message, "utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    return app.config['SLACK_SIGN_VERSION'] + '=' + signature


def check_signature(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        sign = request.headers.get('X-Slack-Signature')
        body = request.get_data().decode("utf-8")

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
