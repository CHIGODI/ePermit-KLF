from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import storage
from web_flask import auth, register, main
from flask_mail import Mail, Message
from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = getenv('SESSION_TYPE')
app.config['SESSION_FILE_DIR'] = getenv('SESSION_FILE_DIR')
app.config['SESSION_FILE_THRESHOLD'] = getenv('SESSION_FILE_THRESHOLD')
app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD') 

#Initialise mail service
mail = Mail(app)

#initilialise session
Session(app)

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(register)

@app.teardown_appcontext
def close_session(exception):
    storage.close()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
