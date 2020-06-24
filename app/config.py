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
