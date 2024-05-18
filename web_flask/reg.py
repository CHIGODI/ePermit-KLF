#!/usr/bin/env python3
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
@token_required
def register_page():
    """ registers a business """  
    return render_template('register.html', cache_id=cache_id)


@register.route('/register/business', methods=['POST'], strict_slashes=False)
@token_required
def register_business():
    """ registers a business """
    categories = storage.all(Category).values()
    if request.method == 'POST':
        kwargs_business = {
            'name': request.form.get('name'),
            'entity_origin': request.form.get('origin'),
            'kra_pin': request.form.get('KRA_pin'),
            'vat_no': request.form.get('vat'),
            'po_box': request.form.get('box'),
            'postal_code': request.form.get('postal_code'),
            'business_telephone': request.form.get('business_telephone'),
            'activity_description': request.form.get('description'),
            'category_id': request.form.get('category_id'),
            'latitude': request.form.get('Latitude'),
            'longitude': request.form.get('longitude'),
        }
        kwargs_owner = {
            'first_name': request.form.get('owner_first_name'),
            'last_name': request.form.get('owner_last_name'),
            'id_number': request.form.get('ID_number'),
            'gender': request.form.get('gender'),
            'designation': request.form.get('designation'),
            'phone_number': request.form.get('phone_number'),
            'signature': request.form.get('signature')
        }
        return render_template('payment.html',
                               kwargs_business=kwargs_business,
                               kwargs_owner=kwargs_owner,
                               categores=categories,
                               cache_id=cache_id)


# get access token to work with daraja API
def get_access_token(consumer_key, consumer_secret):
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print('Failed to obtain access token.')
        return None


@register.route('/pay', methods=['POST', 'GET'], strict_slashes=False)
@token_required
def mpesa_express():
    """ registers a business """
    if request.method == 'POST':
        consumer_key = 'ogBEljyvnKUgUQYyyBDzD1QQqsiQUgxRFI2RrjGramfqv0Qs'
        consumer_secret = '5kZfOqrXAfWFMcBB2hZtNbu4hGwrEWrCrIyWhWWjJ9z85R4lCJtcMwNUAWsE8k0L'
        access_token = get_access_token(consumer_key, consumer_secret)
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + time_stamp
        pwd = b64encode(password.encode("utf-8")).decode("utf-8")
        phone_number = request.form.get('phone_number')
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
        payload = {
        "BusinessShortCode": 174379,
        "Password": pwd,
        "Timestamp": time_stamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,
        "PartyB": 174379,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://1003-102-166-221-241.ngrok-free.app/callback",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
        }
        payload_json = json.dumps(payload)
        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload_json)
        return response.json()
    else:
        return render_template('payment.html')

@register.route('/callback', methods=['POST', 'GET'], strict_slashes=False)
@token_required
def mpesa_callback():
    print('imeingia mpya before')
    data = request.data
    print(data)
    return render_template('payment.html', cache_id=cache_id)
