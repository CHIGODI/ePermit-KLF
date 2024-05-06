#!/usr/bin/python3
""" Module for the API """
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(exception=None):
    """method that closed db session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)