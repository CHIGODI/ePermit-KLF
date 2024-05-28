#!/usr/bin/env python3
""" Module for registering businesses. """

from datetime import datetime
from flask import request, render_template, g, flash, jsonify
import requests
import json
from models.user import User
from models.business import Business
from models import storage
from models.category import Category
from models.permit import Permit
import uuid
from web_flask import register
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from . import token_required
from os import getenv

@register.route('/register', methods=['GET'], strict_slashes=False)
@token_required('user')
def register_page():
    """ renders the register page"""
    current_user = g.get('current_user')
    categories = storage.all(Category).values()

    if current_user and categories:
        user_id = current_user.id
        return render_template('register.html',
                               user_id=user_id,
                               categories=categories)
    else:
        flash(f'Something went wrong!', 'error')
        return render_template('dashboard.html')

@register.route('/pay', methods=['GET'], strict_slashes=False)
@token_required('user')
def mpesa_express():
    """ This function renders payment page. """
    businesses = storage.all(Business).values()
    businesses_bills = [business for business in businesses if business.verified]
    business_ids = [business.id for business in businesses]
    permits = [p for p in storage.all(Permit).values() if p.business_id in business_ids]
    invalid_permits = [permit for permit in permits if not permit.is_valid]
    return render_template('payment.html',
                          businesses_bills=businesses_bills)