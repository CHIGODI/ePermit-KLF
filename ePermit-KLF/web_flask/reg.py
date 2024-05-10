from flask import Flask, request, render_template
import requests
import json
from models.user import User
from models import storage
from models.category import Category
import uuid
from flask import Blueprint
from web_flask import register
from flask_login import login_required

cache_id = uuid.uuid4()

@register.route('/', methods=['GET'], strict_slashes=False)
@login_required
def dashboard():
    """ registers a business """  
    return render_template('dashboard.html', cache_id=cache_id)


@register.route('/register', methods=['GET'], strict_slashes=False)
@login_required
def register_page():
    """ registers a business """  
    return render_template('register.html', cache_id=cache_id)


@register.route('/register/business', methods=['POST'], strict_slashes=False)
@login_required
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

@register.route('/pay', methods=['GET'], strict_slashes=False)
@login_required
def pay():
    """ registers a business """  
    return render_template('payment.html', cache_id=cache_id)













# @app.route('/pay', methods=['POST'])
# def process_form():
#     phone_number = request.form['phone_number']
#     headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer ZZLb2ATpyPZxKqtyjO3jNoYL3jtz'
#     }

#     payload = {
#     "BusinessShortCode": 174379,
#     "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNDMwMjE1NjEx",
#     "Timestamp": "20240430215611",
#     "TransactionType": "CustomerPayBillOnline",
#     "Amount": 1,
#     "PartyA": phone_number,
#     "PartyB": 174379,
#     "PhoneNumber": phone_number,
#     "CallBackURL": "https://mydomain.com/path",
#     "AccountReference": "CompanyXLTD",
#     "TransactionDesc": "Payment of X" 
#     }
#     payload_json = json.dumps(payload)
#     response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload_json)
#     print(response.text.encode('utf8'))
#     return render_template('payment_success.html')

