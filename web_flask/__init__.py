#!/usr/bin/python3
"""__init__.py - initializes the blueprint for the app"""
from flask import Blueprint
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
register = Blueprint('register', __name__)
from web_flask.auth import *
from web_flask.main import *
from web_flask.reg import *

