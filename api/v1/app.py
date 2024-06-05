#!/usr/bin/env python3
""" Module for the API """
from flask_session import Session
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = getenv('SESSION_TYPE')
app.config['SESSION_FILE_DIR'] = getenv('SESSION_FILE_DIR')
app.config['SESSION_FILE_THRESHOLD'] = int(getenv('SESSION_FILE_THRESHOLD'))
app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.register_blueprint(app_views)


CORS(app, resources={r"/*": {"origins": "*"}})
Session(app)
mail = Mail(app)


#This that closes the db session
@app.teardown_appcontext
def close_db(exception=None):
    """method that closed db session"""
    storage.close()


# Error handler for 404 (page not found error)
@app.errorhandler(404)
def not_found(error):
    """method that handle 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("EPERMIT_API_HOST", "0.0.0.0")
    port = getenv("EPERMIT_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)