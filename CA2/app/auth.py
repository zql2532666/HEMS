# Authentication routes

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
# from DbAccess import *
from DynamoDB import * 
import json

auth = Blueprint('auth', __name__)

# Initialise Database
db_access = DynamoDBEngine()

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = db_access.retrieve_user_by_email(email)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    print(len(user))
    print(check_password_hash(user[0]['password'], password))
    if len(user) != 1 or not check_password_hash(user[0]['password'], password):
        flash(u'Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # Create session data, we can access this data in other routes
    session['loggedin'] = True
    session['id'] = user[0]['id']
    session['name'] = user[0]['name']
    session['email'] = user[0]['email']

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.index2'))

@auth.route('/signup')
def signup():
    return render_template("register.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = db_access.retrieve_user_by_email(email)
    if len(user) == 1: # if a user is found, we want to redirect back to signup page so user can try again
        flash(u'Email address already exists', 'danger')
        return redirect(url_for('auth.signup'))

    # if(db_access.insert_new_user(email, name, generate_password_hash(password, method='sha256')) == 0):
        # flash(u'Error occured', 'danger')
        # return redirect(url_for('auth.signup'))
    db_access.insert_new_user(email, name, generate_password_hash(password, method='sha256'))
    flash(u'Successfully registered', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():

    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    session.pop('email', None)

    # Redirect to login page
    return redirect(url_for('auth.login'))