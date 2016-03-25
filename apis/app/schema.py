from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from flask.ext.login import UserMixin
__author__ = 'subham'

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item = db.Column(db.String(120), nullable=False, unique=True)
    isComplete = db.Column(db.Boolean, default=False)

    def __init__(self, item, user_id):
        self.item = item
        self.user_id = user_id

    def json_dump(self):
        return dict(id=self.id, item=self.item, isComplete=self.isComplete)

    def __repr__(self):
        return '<Todo {}>'.format(self.item)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def json_dump(self):
        return dict(id=self.id, email=self.email)

    def __repr__(self):
        return '<Todo {}>'.format(self.email)
