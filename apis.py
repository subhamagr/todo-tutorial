from flask import Flask, jsonify, request
from flask.ext.script import Manager
import os
from schema import db, Todo

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


@app.route('/todos', defaults={'todo_id': 0}, methods=['GET', 'POST', 'PUT'])
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def todos_api(todo_id):
    if request.method == 'GET':
        return throw_todos()

    if request.method == 'POST':
        return add_todo()

    if request.method == 'PUT':
        return mark_complete()

    if request.method == 'DELETE':
        return delete_todo(todo_id)


def throw_todos():
    response = dict()
    todos = Todo.query.all()
    response['todos'] = [todo.json_dump() for todo in todos]
    return jsonify(response), 200


def add_todo():
    item_json = request.json
    item = item_json['item']

    response = dict()

    if item == '':
        response['message'] = 'Invalid'
        return jsonify({'message': 'Invalid'}), 409
    todo_item = Todo(item)
    db.session.add(todo_item)
    db.session.commit()

    response['message'] = 'Todo successfully added'
    return jsonify(response), 201


def mark_complete():
    item_json = request.json
    todo_id = item_json['todo_id']
    is_complete = item_json['is_complete']

    response = dict()
    todo_item = Todo.query.get(todo_id)

    if not todo_item:
        return jsonify({'message': 'Not found'}), 404
    if type(is_complete) != bool:
        return jsonify({'message': 'Invalid complete status'}), 409

    todo_item.isComplete = is_complete

    db.session.commit()

    response['message'] = 'Todo successfully updated'
    return jsonify(response), 201


def delete_todo(todo_id):

    response = dict()
    todo_item = Todo.query.get(todo_id)

    if not todo_item:
        return jsonify({'message': 'Not found'}), 404

    db.session.delete(todo_item)
    db.session.commit()

    response['message'] = 'Todo successfully deleted'
    return jsonify(response), 201


@manager.command
def createdb():
    db.drop_all()
    db.create_all()


@manager.command
def dropall():
    db.drop_all()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Todo=Todo)

if __name__ == '__main__':
    manager.run()
