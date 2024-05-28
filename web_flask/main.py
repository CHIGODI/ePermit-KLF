#!/usr/bin/env python3
""" Main module contains routes to main pages of the Flask app. """

from flask import Blueprint, render_template, request, flash, g
from models import storage
from models.category import Category
from models.permit import Permit
from web_flask import main
from . import token_required

@main.route('/', methods=['GET'], strict_slashes=False)
def landing():
    return render_template('landing_page.html')


@main.route('/dashboard', methods=['GET'], strict_slashes=False)
@token_required('user')
def dashboard():
    """ User dashboard where normal users can register businesses """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    return render_template('services.html', businesses=businesses)

@main.route('/mybusinesses', methods=['GET'], strict_slashes=False)
@token_required('user')
def mybusinesses():
    """ user businesses """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    permits = storage.all(Permit).values()
    return render_template('my_businesses.html',
                           businesses=businesses,
                           permits=permits)

@main.route('/myprofile', methods=['GET'], strict_slashes=False)
@token_required('user')
def myprofile():
    """ user profile """
    current_user = g.get('current_user')
    return render_template('my_profile.html', current_user=current_user)


@main.route('/mypermits', methods=['GET'], strict_slashes=False)
@token_required('user')
def mypermits():
    """ user permits """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    business_ids = [business.id for business in businesses]
    permits = [p for p in storage.all(Permit).values() if p.business_id in business_ids]
    return render_template('my_permits.html', permits=permits)


@main.route('/admin_dashboard', methods=['GET'], strict_slashes=False)
@token_required('admin')
def admin_dashboard():
    """ Admin dashboard where admins can verify business registrations """
    return render_template('admin_dashboard.html')


@main.route('/comingsoon', methods=['GET'], strict_slashes=False)
@token_required('user')
def coming_soon():
    """ These renders a page for all services that are currently not available"""
    return render_template('coming_soon.html')
