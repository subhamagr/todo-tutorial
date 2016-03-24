from flask import Flask
from schema import db

# configuration

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

from app import apis
