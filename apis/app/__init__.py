from flask import Flask
from schema import db
from flask.ext.login import LoginManager

# configuration

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from app import apis
