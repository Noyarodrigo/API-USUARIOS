from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admins, db
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
     create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,get_csrf_token
)
#jwt_refresh_token_required,

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Admins.query.filter_by(User=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.Password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    user_data = {'AdminID':user.AdminID,'pass':user.Password}
    access_token = create_access_token(identity=user_data)
    #refresh_token = create_refresh_token(identity=user_data)

    login_user(user, remember=remember)

    resp = make_response(redirect(url_for('main.index')))
    #resp.headers['csrf_access_token'] = get_csrf_token(access_token)
    #resp.headers['csrf_refresh_token'] = get_csrf_token(refresh_token)
    resp.set_cookie(key='access_token', value=access_token, httponly = True)
    return resp

"""
@auth.route('/token/refresh', methods=['POST'])
#@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Admins.query.filter_by(User=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Admins(User=email, Password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
"""

@auth.route('/logout')
@login_required
def logout():
    resp = make_response(redirect(url_for('main.index')))
    resp.delete_cookie('access_token', path='/', domain=None)
    logout_user()

    return resp
