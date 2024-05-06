#!/usr/bin/python3
""" Module for the API for businesses """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.business import Business


@app_views.route('/businesses', methods=['GET'], strict_slashes=False)
def get_businesses():
    """ method that retrieves all businesses """
    businesses = storage.all(Business).values()
    businesses_list = []
    businesses_list = [business.to_dict() for business in businesses]
    return jsonify(businesses_list)


@app_views.route('/businesses/<business_id>', methods=['GET'], strict_slashes=False)
def get_business(business_id):
    """ method that retrieves a business """
    business = storage.get(Business, business_id)
    if business is None:
        abort(404)
    return jsonify(business.to_dict())


@app_views.route('/businesses/<business_id>', methods=['DELETE'], strict_slashes=False)
def delete_business(business_id):
    """ method that deletes a business """
    business = storage.get(Business, business_id)
    if business is None:
        abort(404)
    storage.delete(business)
    storage.save()
    return jsonify({}), 200


@app_views.route('/businesses', methods=['POST'], strict_slashes=False)
def create_business():
    """ method that creates a business """
    business_json = request.get_json()
    if business_json is None:
        abort(400, "Not a JSON")
    if 'name' not in business_json:
        abort(400, "Missing name")
    if 'description' not in business_json:
        abort(400, "Missing description")
    if 'category_id' not in business_json:
        abort(400, "Missing category_id")
    if 'user_id' not in business_json:
        abort(400, "Missing user_id")
    if 'address' not in business_json:
        abort(400, "Missing address")
    if 'KRA_pin' not in business_json:
        abort(400, "Missing KRA-pin")
    business = Business(**business_json)
    storage.new(business)
    storage.save()
    return jsonify(business.to_dict()), 201


@app_views.route('/businesses/<business_id>', methods=['PUT'], strict_slashes=False)
def update_business(business_id):
    """ method that updates a business """
    business = storage.get(Business, business_id)
    if business is None:
        abort(404)
    business_json = request.get_json()
    if business_json is None:
        abort(400, "Not a JSON")
    for key, value in business_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(business, key, value)
    storage.save()
    return jsonify(business.to_dict())
