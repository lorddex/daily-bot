from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

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
