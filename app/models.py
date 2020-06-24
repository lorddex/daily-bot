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

import datetime

from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), index=True, unique=False, nullable=False)
    channel = db.Column(db.String(), index=False, unique=False, nullable=True)
    ts = db.Column(db.String(), index=False, unique=False, nullable=True)
    created = db.Column(db.DateTime(), index=True, nullable=False, default=datetime.datetime.now)
