#!/usr/bin/env python3
""" checks validity of permit """

from models.permit import Permit
from models.business import Business
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort



app_views.route('/validity/<permit_id>', methods=['POST'], strict_slashes=False)
def check_validity(permit_id):
    """  returns json with status of permit """
    permit = storage.get_obj_by_id(Permit, permit_id)

    if not permit:
        abort(404, )
    else:
        if permit.check_validity():
            return jsonify({'status': 'valid'}), 200
        else:
            return jsonify({'status': 'expired'}), 200
