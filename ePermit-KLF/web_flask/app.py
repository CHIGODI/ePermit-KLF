from flask import Flask, request, render_template
import requests
import json
from models.user import User
from models import storage
from models.category import Category
import uuid


app = Flask(__name__)

cache_id = uuid.uuid4()


@app.route('/register', methods=['POST', 'GET'], strict_slashes=False)
def register_page():
    """ registers a business """  
    return render_template('register.html', cache_id=cache_id)


@app.route('/register/business', methods=['POST'], strict_slashes=False)
def register_business():
    """ registers a business """
    if request.method == 'POST':
        business_name =request.form.get('name')
        description = request.form.get('description')
        categories = storage.all(Category)    
        return render_template('payment.html', categores=categories, cache_id=cache_id)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)












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

