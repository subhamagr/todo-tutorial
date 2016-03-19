from flask import Flask, jsonify
from flask.ext.script import Manager
import os
from schema import db

# configuration
DEBUG = True
SECRET_KEY = 'this-is-a-secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['TODODB'])
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
db.init_app(app)

manager = Manager(app)


@app.route('/')
def index():
    response = dict()
    response['message'] = 'Hello world'
    return jsonify(response)


@manager.command
def createdb():
    db.drop_all()
    db.create_all()


@manager.command
def dropall():
    db.drop_all()

if __name__ == '__main__':
    manager.run()
