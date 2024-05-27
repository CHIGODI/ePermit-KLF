#!/usr/bin/env python3

from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
from flask import render_template, redirect, url_for, session, g
from flask import request, flash, jsonify, make_response, current_app
from functools import wraps
from os import getenv
from web_flask import auth
from models.user import User
from models import storage

load_dotenv()

def token_required(role):
    """ Decorator function to check if token is passed """
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            """ Decorator function to check if token is passed """
            token = request.cookies.get('x-access-token')
            if not token:
                flash('Please Login to access!', 'error')
                return redirect(url_for('auth.login'))

            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, getenv('SECRET_KEY'),
                                algorithms=['HS256'])
                current_user = storage.get_obj_by_id(User, data['id'])
                g.current_user = current_user

                if not current_user.has_role(role):
                    flash('You do not have permission to access this resource.', 'error')
                    return redirect(url_for('auth.login'))

            except jwt.ExpiredSignatureError:
                flash('Your Session has expired.', 'error')
                return redirect(url_for('auth.login'))
            except jwt.InvalidTokenError:
                flash('Invalid token. Please log in.', 'error')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash('Something went wrong. Please try again!', 'error')
                return redirect(url_for('auth.login'))
            return func(*args, **kwargs)
        return decorated
    return decorator
