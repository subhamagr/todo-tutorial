from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
__author__ = 'subham'

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    isComplete = db.Column(db.Boolean, default=False)

    def __init__(self, item):
        self.item = item

    def json_dump(self):
        return dict(id=self.id, item=self.item, isComplete=self.isComplete)

    def __repr__(self):
        return '<Todo {}>'.format(self.item)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def json_dump(self):
        return dict(id=self.id, email=self.email)

    def __repr__(self):
        return '<Todo {}>'.format(self.item)
