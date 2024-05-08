from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import storage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'epermit_secret_key'

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return storage.get(User, user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)