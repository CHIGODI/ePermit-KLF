#!/usr/bin/env python3
""" Module for the API """
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.config['SECREY_KEY'] = getenv('SECRET_KEY')
app.register_blueprint(app_views) # Register the blueprint
CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS


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
    app.run(host=host, port=port, threaded=True, debug=True)