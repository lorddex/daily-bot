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

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import Message

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def delete_all_messages():
    messages_query = db.session.query(Message)
    app.logger.warning('Removing {} elements'.format(messages_query.count()))
    messages_query.delete()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
