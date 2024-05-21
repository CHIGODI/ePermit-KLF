#!/usr/bin/env python3
""" Module for registering businesses. """

from datetime import datetime
from flask import request, render_template
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

cache_id = uuid.uuid4()


@register.route('/register', methods=['GET'], strict_slashes=False)
# @token_required
def register_page():
    """ renders the register page"""
    return render_template('register.html', cache_id=cache_id)


@register.route('/pay/', methods=['GET'], strict_slashes=False)
# @token_required
def mpesa_express():
    """ This function initiates a payment request to the M-Pesa API. """
    return render_template('payment.html')