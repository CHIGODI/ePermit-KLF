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
        print(user_id)
        return render_template('register.html',
                               user_id=user_id,
                               categories=categories)
    else:
        print('here')
        flash(f'Something went wrong!', 'error')
        return render_template('dashboard.html')

@register.route('/pay', methods=['GET'], strict_slashes=False)
@token_required('user')
def mpesa_express():
    """ This function renders payment page. """
    current_user = g.get('current_user')
    businesses = [business for business in current_user.businesses if business.verified]
    business_ids = [business.id for business in businesses]

    print(businesses)
    permits = []
    new_businesses = []
    for business_id in business_ids:
        permit = storage.get_permit_by_business_id(business_id)
        if permit:
            permits.append(permit)
        else:
            new_businesses.append(business_id)

    print(permits)
    if not permits:
        return render_template('payment.html',
                               new_businesses=new_businesses)
    else:
        bswithexpired_permits = []
        for permit in permits:
            if permit.check_validity() is False:
                business = storage.get_obj_by_id(Business, permit.business_id)
                bswithexpired_permits.append(business)
        
        bswithexpired_permits.extend(new_businesses)
        return render_template('payment.html',
                            bswithexpired_permits=bswithexpired_permits)
