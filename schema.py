from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'subham'

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    isComplete = db.Column(db.Boolean, default=False)

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return '<Todo {}>'.format(self.item)
