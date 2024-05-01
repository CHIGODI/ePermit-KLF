from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    return render_template('landing_page.html')


@app.route('/signup', strict_slashes=False)
def sign_up():
    return render_template('sign_up.html')


@app.route('/pay', methods=['POST'])
def process_form():
    phone_number = request.form['phone_number']
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ZZLb2ATpyPZxKqtyjO3jNoYL3jtz'
    }

    payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNDMwMjE1NjEx",
    "Timestamp": "20240430215611",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": phone_number,
    "PartyB": 174379,
    "PhoneNumber": phone_number,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
    }
    payload_json = json.dumps(payload)
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload_json)
    print(response.text.encode('utf8'))
    return render_template('payment_success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




# import requests
# ​
# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'Bearer ZZLb2ATpyPZxKqtyjO3jNoYL3jtz'
# }
# ​
# payload = {
#     "BusinessShortCode": 174379,
#     "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNTAxMTMzMDEz",
#     "Timestamp": "20240501133013",
#     "TransactionType": "CustomerPayBillOnline",
#     "Amount": 1,
#     "PartyA": 254708374149,
#     "PartyB": 174379,
#     "PhoneNumber": 254708374149,
#     "CallBackURL": "https://mydomain.com/path",
#     "AccountReference": "CompanyXLTD",
#     "TransactionDesc": "Payment of X" 
#   }
# ​
# response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
# print(response.text.encode('utf8'))