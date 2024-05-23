#!/usr/bin/env python3
""" Main module contains routes to main pages of the Flask app. """

from flask import Blueprint, render_template, request, flash, g
from web_flask import main
from . import token_required

@main.route('/', methods=['GET'], strict_slashes=False)
def landing():
    return render_template('landing_page.html')


@main.route('/dashboard', methods=['GET'], strict_slashes=False)
@token_required('user')
def dashboard():
    """ User dashboard where normal users can register businesses """
    return render_template('services.html')


@main.route('/admin_dashboard', methods=['GET'], strict_slashes=False)
@token_required('admin')
def admin_dashboard():
    """ Admin dashboard where admins can verify business registrations """
    return render_template('admin_dashboard.html')


@main.route('/comingsoon', methods=['GET'], strict_slashes=False)
@token_required
def comingsoon():
    """ These renders a page for all services that are currently not available"""
    return render_template('coming_soon.html')