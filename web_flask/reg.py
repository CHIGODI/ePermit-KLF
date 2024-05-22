#!/usr/bin/env python3
""" Module for registering businesses. """

from datetime import datetime
from flask import request, render_template, g, flash
import requests
import json
from models.user import User
from models import storage
from models.category import Category
import uuid
from web_flask import register
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from . import token_required

@register.route('/register', methods=['GET'], strict_slashes=False)
@token_required('user')
def register_page():
    """ renders the register page"""
    current_user = g.get('current_user')
    categories = storage.all(Category).values()

    for  category in categories:
        print(category.id)
    if current_user:
        user_id = current_user.id
        return render_template('register.html',
                               user_id=user_id,
                               categories=categories)
    else:
        flash(f'Something went wrong!', 'error')
        return render_template('dashboard.html')


@register.route('/pay/', methods=['GET'], strict_slashes=False)
@token_required('user')
def mpesa_express():
    """ This function initiates a payment request to the M-Pesa API. """
    return render_template('payment.html')