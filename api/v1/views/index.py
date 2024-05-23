#!/usr/bin/python3
""" Module for the API """
from api.v1.views import app_views
from flask import jsonify


#This route retrieves the status of the API
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ method that returns a JSON status of the API"""
    return jsonify({"status": "OK"})


# This is the new route that will be added to the API to get the number of objects by type
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ method that retrieves the number of each objects by type """
    from models import storage
    count_stats = {"user": storage.count("User"),
               "business": storage.count("Business"),
               "category": storage.count("Category"),
               "permit": storage.count("Permit"),
               }

    return jsonify(count_stats)
