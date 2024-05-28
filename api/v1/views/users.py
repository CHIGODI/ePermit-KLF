#!/usr/bin/python3
""" Module for the API  users """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.token import token_required


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ method that retrieves all users """
    users = storage.all(User).values()
    users_list = []
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ method that retrieves a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ method that deletes a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ method that creates a user """
    user_json = request.get_json()
    if user_json is None:
        abort(400, "Not a JSON")
    if 'email' not in user_json:
        abort(400, "Missing email")
    if 'password' not in user_json:
        abort(400, "Missing password")
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ method that updates a user """
    user = storage.get_obj_by_id(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        abort(400, "Not a JSON")
    for key, value in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
