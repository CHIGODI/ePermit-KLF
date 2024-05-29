#!/usr/bin/env python3


from datetime import datetime
from flask import request, render_template, g, flash, jsonify, session, make_response
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
from os import getenv
from api.v1.views import app_views
from dotenv import load_dotenv
from models.permit import Permit
from models.mpesa import Mpesa



# loading environment variables
load_dotenv()

# get access token to work with daraja API
def get_access_token(consumer_key, consumer_secret):
    """ Get access token to work with daraja API """
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

@app_views.route('/paympesa', methods=['POST'], strict_slashes=False)
def stkPush():
    """ This function initiates a payment request to the M-Pesa API. """
    try:
        access_token = get_access_token(getenv('CONSUMER_KEY'),
                                        getenv('CONSUMER_SECRET'))
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        Shortcode = getenv('SHORT_CODE')
        Passkey = getenv('PASS_KEY')
        password = Shortcode + Passkey + time_stamp
        pwd = b64encode(password.encode("utf-8")).decode("utf-8")
        data = request.get_json()
        phone  = data.get('phone_number')
        phone_number = phone[1:10]
        session['business_id'] = request.form.get('business_id')

        if not access_token:
            return  jsonify({"status": "Error. Please try again."}), 500

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
        payload = {
        "BusinessShortCode": Shortcode,
        "Password": pwd,
        "Timestamp": time_stamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": f'254{phone_number}',
        "PartyB": Shortcode,
        "PhoneNumber": f'254{phone_number}',
        "CallBackURL": "https://www.epermit.live/api/v1/callback",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment for Permit"
        }
        payload_json = json.dumps(payload)
        response = requests.request("POST",
                                    'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                    headers = headers,
                                    data = payload_json)
        r = response.json()
        session['CheckoutRequestID'] = r.get('CheckoutRequestID')
        return  make_response(jsonify(r), 200)
    except:
        return jsonify({"status": "Error. Please try again."}), 500


@app_views.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    """ This function receives the callback from the M-Pesa API. """
    response = request.get_json()
    result_code = response.get('Body').get('stkCallback').get('ResultCode')

    if result_code == 0:
        TransactionDate = response.get('Body').get('stkCallback').get('CallbackMetadata').get('Item')[2].get('Value')
        Amount = response.get('Body').get('stkCallback').get('CallbackMetadata').get('Item')[0].get('Value')
        MpesaReceiptNumber = response.get('Body').get('stkCallback').get('CallbackMetadata').get('Item')[1].get('Value')
        PhoneNumber =  response.get('Body').get('stkCallback').get('CallbackMetadata').get('Item')[3].get('Value')
        business_id = session.get('business_id')
        
        kwargs_permit = {
            'business_id': business_id,
        }
        
        new_permit = Permit(**kwargs_permit)
        kwargs = {
            'TransactionDate': TransactionDate,
            'Amount':  Amount,
            'MpesaReceiptNumber': MpesaReceiptNumber,
            'PhoneNumber': PhoneNumber,
            'permit_id': new_permit.id
        }
        save_transaction = Mpesa(**kwargs)
        new_permit.save()
        save_transaction.save()
        session.pop('business_id', None)
        return jsonify({"status": "ok"})
    else:
        return jsonify({'ResultCode': result_code})


@app_views.route('/stkquery', methods=['GET'], strict_slashes=False)
def stkQuery():
    """ This function checks the status of a payment request to the M-Pesa API. """
    try:
        access_token = get_access_token(getenv('CONSUMER_KEY'),
                                        getenv('CONSUMER_SECRET'))
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        Shortcode = getenv('SHORT_CODE')
        Passkey = getenv('PASS_KEY')
        password = Shortcode + Passkey + time_stamp
        pwd = b64encode(password.encode("utf-8")).decode("utf-8")

        if not access_token:
            return  jsonify({"status": "Error. Please try again."}), 500

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
        payload = {
        "BusinessShortCode": Shortcode,
        "Password": pwd,
        "Timestamp": time_stamp,
        "CheckoutRequestID": session.get('CheckoutRequestID')
        }
        payload_json = json.dumps(payload)
        response = requests.request("POST",
                                    'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
                                    headers = headers,
                                    data = payload_json)
        r = response.json()
        session.pop('CheckoutRequestID', None)
        return  make_response(jsonify(r), 200)
    except:
        return jsonify({"status": "fail"}), 500
