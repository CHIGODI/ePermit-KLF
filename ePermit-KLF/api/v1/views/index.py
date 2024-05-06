#!/usr/bin/python3
""" Module for the API """
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ method that returns a JSON """
    return jsonify({"status": "OK"})

