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


@app.route('/todos', methods=['GET'])
def todos():
    response = dict()
    todos = Todo.query.all()
    response['todos'] = [todo.json_dump() for todo in todos]
    return jsonify(response), 200


@app.route('/add', methods=['POST'])
def add():
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


@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete(todo_id):

    response = dict()
    todo_item = Todo.query.get(todo_id)

    if not todo_item:
        response['message'] = 'Invalid'
        return jsonify({'message': 'Invalid'}), 409

    db.session.delete(todo_item)
    db.session.commit()

    response['message'] = 'Todo successfully deleted'
    return jsonify(response), 201


@app.route('/complete', methods=['PUT'])
def complete():
    item_json = request.json
    todo_id = item_json['todo_id']
    is_complete = item_json['is_complete']

    response = dict()
    todo_item = Todo.query.get(todo_id)

    if not todo_item or type(is_complete) != bool:
        response['message'] = 'Invalid'
        return jsonify({'message': 'Invalid'}), 409

    todo_item.isComplete = is_complete

    db.session.commit()

    response['message'] = 'Todo successfully updated'
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
