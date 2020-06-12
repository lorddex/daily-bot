import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SLACK_SIGN_SECRET = os.environ.get('SLACK_SIGN_SECRET', '')
    SLACK_SIGN_VERSION = 'v0'
    SLACK_OAUTH_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN', '')
    SLACK_WORKSPACE = os.environ.get('SLACK_WORKSPACE', '')

    SLACK_VERIFICATION_ENABLED = os.environ.get('SLACK_VERIFICATION_ENABLED', False)
