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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.Config'
)
app.config.from_object(app_settings)
db = SQLAlchemy(app)

from app import views
