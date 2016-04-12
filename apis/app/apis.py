from flask import jsonify, request, g
from schema import Todo, User
from helpers import InvalidApiUsage
from app import app, db, auth


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        g.user = user
        return True
    else:
        raise InvalidApiUsage('Unauthorized access', 401)


@app.route('/register', methods=['POST'])
def register():
    json = request.json
    email = json['email']
    password = json['password']

    user = User.query.filter_by(email=email).first()
    if user:
        raise InvalidApiUsage('User with same email id already exists', 409)
    else:
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Account successfully created'})


@app.route('/todos', defaults={'todo_id': 0}, methods=['GET', 'POST', 'PUT'])
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@auth.login_required
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
    todos = Todo.query.filter_by(user_id=g.user.id).all()
    response['todos'] = [todo.json_dump() for todo in todos]
    return jsonify(response), 200


def add_todo():
    item_json = request.json
    item = item_json['item']

    response = dict()

    if item == '':
        response['message'] = 'Invalid'
        raise InvalidApiUsage('Invalid', 409)
    user = g.user
    todo_item = Todo(item, user.id)
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

    user = g.user
    if not todo_item:
        raise InvalidApiUsage('Not found', 404)
    if todo_item.user_id != user.id:
        raise InvalidApiUsage('Unauthorized', 403)
    if type(is_complete) != bool:
        raise InvalidApiUsage('Invalid complete status', 409)

    todo_item.isComplete = is_complete

    db.session.commit()

    response['message'] = 'Todo successfully updated'
    return jsonify(response), 201


def delete_todo(todo_id):
    response = dict()
    todo_item = Todo.query.get(todo_id)
    user = g.user
    if not todo_item:
        raise InvalidApiUsage('Not found', 404)
    if todo_item.user_id != user.id:
        raise InvalidApiUsage('Unauthorized', 403)

    db.session.delete(todo_item)
    db.session.commit()

    response['message'] = 'Todo successfully deleted'
    return jsonify(response), 201


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': "Not Found"}), 404
