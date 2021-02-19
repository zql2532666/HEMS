import json, requests
from functools import wraps
from time import sleep
from DbAccess import *
from threading import Thread
from raspberry import *
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash, send_file, session
import os
from auth import *
from main import *
from DynamoDB import *

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise Database
db_access = DynamoDBEngine()

# For testing purposes with jinja. Remove later
# Usage: {{ mdebug("whatever to print here") }}
@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)

# Decorator for registering routes for login
def register_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Check if user is loggedin
        if 'loggedin' not in session:
            # User not logged in, redirect to login page
            flash(u'Log in first', 'danger')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    try:

        # blueprint for auth routes in our app
        app.register_blueprint(auth)

        # blueprint for non-auth parts of app
        app.register_blueprint(main)

        # threads for the sensors
        dht11_thread = Thread(target=run_dht11_sensor)
        light_thread = Thread(target=run_light_sensor)
        dht11_thread.start()
        light_thread.start()

        # server connections
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        app.debug = True
        print('Waiting for requests.. ')
        http_server.serve_forever()

    except:
        print("Exception")

