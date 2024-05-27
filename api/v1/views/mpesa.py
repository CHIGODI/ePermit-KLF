#!/usr/bin/env python3
""" Module for registering businesses. """

from datetime import datetime
from flask import request, jsonify
import requests
import json
from models.user import User
from models import storage
from models.category import Category
import uuid
from web_flask import register
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from api.v1.views import app_views
from os import getenv



@app_views.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    """ This function receives the callback from the M-Pesa API. """
    response = request.get_json()
    result_code = response.get('Body').get('stkCallback').get('ResultCode')
    print(result_code)
    return response