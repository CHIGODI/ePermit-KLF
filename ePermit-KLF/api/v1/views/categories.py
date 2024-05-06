#!/usr/bin/python3
""" Module for the API for categories """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.category import Category


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
def get_categories():
    """ method that retrieves all categories """
    categories = storage.all(Category).values()
    categories_list = []
    categories_list = [category.to_dict() for category in categories]
    return jsonify(categories_list)

@app_views.route('/categories/<category_id>', methods=['GET'], strict_slashes=False)
def get_category(category_id):
    """ method that retrieves a category """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    return jsonify(category.to_dict())

@app_views.route('/categories/<category_id>', methods=['DELETE'], strict_slashes=False)
def delete_category(category_id):
    """ method that deletes a category """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    storage.delete(category)
    storage.save()
    return jsonify({}), 200


@app_views.route('/categories', methods=['POST'], strict_slashes=False)
def create_category():
    """ method that creates a category """
    category_json = request.get_json()
    if category_json is None:
        abort(400, "Not a JSON")
    if 'category_name' not in category_json:
        abort(400, "Missing name")
    if 'fee' not in category_json:
        abort(400, "Missing fee")
    category = Category(**category_json)
    storage.new(category)
    storage.save()
    return jsonify(category.to_dict()), 201


@app_views.route('/categories/<category_id>', methods=['PUT'], strict_slashes=False)
def update_category(category_id):
    """ method that updates a category """
    category = storage.get(Category, category_id)
    if category is None:
        abort(404)
    category_json = request.get_json()
    if category_json is None:
        abort(400, "Not a JSON")
    for key, value in category_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(category, key, value)
    storage.save()
    return jsonify(category.to_dict()), 200
