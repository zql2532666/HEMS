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

# Initialise Database
db_access = DynamoDBEngine()

# Create boto3 client to access aws services
s3_client = boto3.client('s3', region_name='us-east-1')
rek_client=boto3.client('rekognition', region_name='us-east-1')

# Declaring objects
collectionId='mycollection' #collection name (for rekognition)
bucket = 'indexed-faces-iot' #S3 bucket name (for s3)

all_objects = s3_client.list_objects(Bucket=bucket)
list_response = rek_client.list_collections(MaxResults=2)

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

def index_faces():
    '''
    delete existing collection if it exists
    '''
    if collectionId in list_response['CollectionIds']:
        rek_client.delete_collection(CollectionId=collectionId)

    '''
    create a new collection 
    '''
    rek_client.create_collection(CollectionId=collectionId)

    '''
    add all images in current bucket to the collections
    use folder names as the labels
    '''
    for content in all_objects['Contents']:
        collection_name,collection_image =content['Key'].split('/')
        if collection_image:
            label = collection_name
            print('indexing: ',label)
            image = content['Key']    
            index_response=rek_client.index_faces(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':bucket,'Name':image}},
                                    ExternalImageId=label,
                                    MaxFaces=1,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['ALL'])

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

        # register faces for rekognition
        index_faces()

        http_server.serve_forever()

    except:
        print("Exception")

