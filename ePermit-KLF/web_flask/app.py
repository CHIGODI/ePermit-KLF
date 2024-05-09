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