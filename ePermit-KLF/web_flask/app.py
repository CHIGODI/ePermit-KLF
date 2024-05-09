from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import storage
from web_flask import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'epermit_secret_key'

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(register)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    #use the storage class to get the user by id
    return storage.get(User, user_id)

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

