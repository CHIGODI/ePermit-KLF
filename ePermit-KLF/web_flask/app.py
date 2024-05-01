from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from models.user import User
from models import storage
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "epermit_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)

@app.route('/', strict_slashes=False)
def index():
    return render_template('landing_page.html')

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def sign_up():
    if request.method == 'POST':
        user = User(email=request.form.get("email"),
                    password=request.form.get("password"))
        if request.form.get('password') != request.form.get("confirm_password"):
            flash('Passwords do not match')
        else:
            user.save()
            flash('Account created successfully')
            return redirect(url_for("signin"))
    return render_template("sign_up.html")
        
        
@app.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def signin():
    """ Sign in route """
    if request.method == "POST":
        users = storage.all(User) # returns a list of all users objects
        if users:
            for user in users:
                if user.email == request.form.get("email"):
                    if user.password == request.form.get("password"):
                        login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("landing_page.html")


@app.route('/dashboard', strict_slashes=False)
def dashboard():
    return render_template("dashboard.html")


@app.route('/password/reset', strict_slashes=False)
def change_password():
    return render_template('forgot_password.html')

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