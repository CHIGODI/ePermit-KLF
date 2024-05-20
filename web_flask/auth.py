#!/usr/bin/env python3
""" 
This module contains routes for user authentication and authorisation
"""

from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
from flask import render_template, redirect, url_for, session
from flask import request, flash, jsonify, make_response, current_app
from flask_mail import Message
from functools import wraps
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
from web_flask import auth
from models.user import User
from models import storage
import random
import string

#loading environment variables
load_dotenv()


def token_required(func):
    """ Decorator function to check if token is passed """
    @wraps(func)
    def decorated(*args, **kwargs):
        """ Decorator function to check if token is passed """
        token = request.cookies.get('x-access-token')

        # return 401 if token is not passed
        if not token:
            return make_response(jsonify({'message' : 'Token is missing !!'}), 401)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
            current_user = storage.get_user_by_id(User, data['id'])
            # kwargs['current_user'] = current_user
    
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  func(*args, **kwargs)
    return decorated


@auth.route('/login/', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """ This route authorises users to login and access protected routes """
    if request.method == 'POST':
        auth = request.form
        if not auth or not auth.get('email') or not auth.get('password'):
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('auth.login'))
        
        user = storage.get_user_by_email(auth.get('email'))
        if not user:
            flash('Could not verify. User with this email doesn\'t exist.', 'error')
            return redirect(url_for('auth.login'))
        
        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, getenv('SECRET_KEY'), algorithm='HS256')
            
            response = make_response(redirect(url_for('main.dashboard')))
            
            # Set HTTP-only cookie
            response.set_cookie('x-access-token', token, httponly=True, max_age=1800) 
            return response
        
        flash("Wrong email or password.", 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')


def generate_verification_code(length=6):
    """ generate an email verifictaion code """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@auth.route('/signup/', methods=['POST', 'GET'])
def signup():
    """ This route allows users to create an account """
    if request.method == 'POST':     
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pwd = request.form.get('confirm_password')

        # Validate form data
        if not email or not password or not confirm_pwd:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('auth.signup'))
        
        #password length must be 8 chars
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('auth.signup'))
        
        if password != confirm_pwd:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))

        # Check for existing user
        user = storage.get_user_by_email(email)
        if user:
            flash('User with the same email already exists. Please log in.', 'error')
            return redirect(url_for('auth.signup'))
        
        verification_code = generate_verification_code()
        timestamp = datetime.utcnow()

        # Store verification code and timestamp  and user details in Flask session
        session['verification_data'] = {
            'email': email,
            'password': generate_password_hash(password),
            'verification_code': verification_code,
            'timestamp': timestamp.isoformat()
        }

        # Send email with verification code
        msg = Message('Verification ePermit',
                  sender='chiegody254@gmail.com',
                  recipients=[email])
        msg.body = f'Your verification code is: {verification_code}'
        current_app.extensions['mail'].send(msg)

        flash('An email with the verification code has been '
              'sent to your email address. '
              'Code expires after 5 minutes', 'success')

        return redirect(url_for('auth.verify_email'))
    
    return make_response(render_template('sign_up.html'), 200)


@auth.route('/verify_email/', methods=['POST', 'GET'], strict_slashes=False)
def verify_email():
    """ This route allows users to verify their email address """
    if request.method == 'POST':
        data = session.get('verification_data')
        verification_code = request.form.get('verification_code')
        
        
        if not data or data.get('verification_code') != verification_code:
            flash('Invalid verification code.', 'error')
            return redirect(url_for('auth.verify_email'))
        
        # Convert timestamp strings to datetime objects
        timestamp = datetime.fromisoformat(data.get('timestamp'))
        current_time = datetime.utcnow()

        # Calculate time difference
        time_diff = current_time - timestamp

        # if time diff is more that 5 minutes / verification code expired
        if time_diff.total_seconds() > 300:
            flash('Verification code expired. Account creation was not successful.', 'error')
            session.pop('verification_data', None)
            return redirect(url_for('auth.signup'))
        
        # Create user 
        user = User(
            email=data.get('email'),
            password=data.get('password')
        )
        
        # saving user after they verify themselves/persists to DB
        user.save()
        
        flash('Your email has been verified successfully. Please Login', 'success')
        # Clear verification data from session after verification
        session.pop('verification_data', None)
        
        return redirect(url_for('auth.login'))
    return render_template('verify_email.html')


@auth.route('/logout/', methods=['GET'])
def logout():
    """ This route logs out users """
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('x-access-token', '', expires=0)
    flash('You have been logged out successfully.', 'success')
    return response


@auth.route('/forgot_password/', methods=['GET', 'POST'], strict_slashes=False)
def forgot_password(): 
    """ Route for requesting password reset """   
    if request.method == 'POST':
        email = request.form.get('email')
        
        print('email')
        
        if not email:
            flash('Please fill out missing field', 'error')
        
        user = storage.get_user_by_email(email)
        if user:
            # Generate token
            token = jwt.encode({
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, getenv('SECRET_KEY'), algorithm='HS256')
            
            # Send reset email set with a JWT
            password_reset_link = url_for('auth.reset_password', token=token, _external=True)
            message = Message('Password Reset ePermit',
                              sender=getenv('MAIL_USERNAME'),
                              recipients=[email])
            message.body = f'Click the link to reset your password: {password_reset_link} '\
                'If you did not make this request then simply ignore this email and no changes will be made.'
            current_app.extensions['mail'].send(message)
            
            flash('Password reset email sent. Check email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email address not found.', 'error')
    return render_template('forgot_password.html')


@auth.route('/reset_password/', methods=['GET', 'POST'], strict_slashes=flash)
def reset_password(token):
    """ Route for handling password reset """
    token = request.args.get('token')
    try:
        data = jwt.decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
        email = data.get('email')
        user = storage.get_user_by_email(email)
    except jwt.ExpiredSignatureError:
        flash('The reset link has expired.', 'error')
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        flash('Invalid token.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_new_password = request.form.get('confirm_new_password')
        
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('auth.reset_password'))
            
        if new_password != confirm_new_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('reset_password'))
        
        user.password = generate_password_hash(new_password)
        user.save()
        flash('Password updated successfully.')
        return redirect(url_for('login'))
    return render_template('reset_password.html')
