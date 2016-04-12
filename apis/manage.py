from app import app, db
from app.schema import Todo, User
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


# create our little application
manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)
manager.add_command('db', MigrateCommand)


@manager.command
def createdb():
    db.drop_all()
    db.create_all()


@manager.command
def dropall():
    db.drop_all()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Todo=Todo, User=User)

if __name__ == '__main__':
    manager.run()
