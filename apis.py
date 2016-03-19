from flask import Flask, jsonify
import os

# configuration
DEBUG = True
SECRET_KEY = 'this-is-a-secret-key'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    response = dict()
    response['message'] = 'Hello world'
    return jsonify(response)
    

if __name__ == '__main__':
    app.run()
