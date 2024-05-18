from flask import render_template, redirect, url_for, request, flash, jsonify, make_response, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import storage
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps
from web_flask import auth
from os import getenv
import random
import string
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('x-access-token')

        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
            current_user = storage.get_user_by_id(User, data['id'])
           
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  func(*args, **kwargs)
    return decorated


@auth.route('/login', methods=['POST', 'GET'], strict_slashes=False)
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
        
        flash("Wrong email or password. Don't have an account?", 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')


def generate_verification_code(length=6):
    """ generate an email verifictaion code """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    """ """
    if request.method == 'POST':     
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pwd = request.form.get('confirm_password')

        # Validate form data
        if not email or not password or not confirm_pwd:
            flash('Please fill out all fields.')
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

        # Store verification code and timestamp  and user details in session
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

        flash('An email with the verification code has been sent to your email address. Code expires after 5 minutes', 'success')
        return redirect(url_for('auth.verify_email'))
    
    return make_response(render_template('sign_up.html'), 200)

@auth.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
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

@auth.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('x-access-token', '', expires=0)
    flash('You have been logged out successfully.', 'success')
    return response