from flask import Flask
from schema import db
from flask_httpauth import HTTPBasicAuth


# configuration

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
auth = HTTPBasicAuth()

from app import apis
