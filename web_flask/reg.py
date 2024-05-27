#!/usr/bin/env python3
""" Module for registering businesses. """

from datetime import datetime
from flask import request, render_template, g, flash, jsonify
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


# get access token to work with daraja API
def get_access_token(consumer_key, consumer_secret):
    """ Get access token to work with daraja API """
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None


@register.route('/pay/', methods=['POST', 'GET'], strict_slashes=False)
@token_required('user')
def mpesa_express():
    """ This function initiates a payment request to the M-Pesa API. """
    if request.method == 'POST':
        access_token = get_access_token(getenv('CONSUMER_KEY'),
                                        getenv('CONSUMER_SECRET'))
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + time_stamp
        pwd = b64encode(password.encode("utf-8")).decode("utf-8")
        phone_number = request.form.get('phone_number')

        if not phone_number:
            flash('Please provide a phone number.', 'error')
            return render_template('payment.html')

        if not access_token:
            flash('Payment failed. Please try again.', 'error')
            return render_template('payment.html')

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
        "CallBackURL": "https://www.epermit.live/callback",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
        }
        payload_json = json.dumps(payload)
        response = requests.request("POST",
                                    'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                    headers = headers,
                                    data = payload_json)
        r = response.json()
        response_code = r.get('ResponseCode')
        if response_code != '0':
            flash('Payment failed. Please try again.', 'error')
            return render_template('payment.html')
        else:
            flash('Payment request sent successfully!', 'success')
            return render_template('waiting_page.html')
    return render_template('payment.html')


@register.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    """ This function receives the callback from the M-Pesa API. """
    response = request.get_json()

    print('success!')
    result_code = response.get('Body').get('stkCallback').get('ResultCode')
    if result_code != '0':
        print('failed')
        flash('Payment failed or was cancelled. Please try again.', 'error')
        return render_template('payment.html')
    else:
        print('not triggering')
        flash('Payment successful. Your business has been registered.', 'success')
        return render_template('my_permits.html')
