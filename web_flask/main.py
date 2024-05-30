#!/usr/bin/env python3
""" Main module contains routes to main pages of the Flask app. """

from flask import Blueprint, render_template, request, flash, g, redirect, url_for
from models import storage
from models.category import Category
from models.permit import Permit
from models.business import Business
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

    print(permits)
    return render_template('my_permits.html', permits=permits)


@main.route('/comingsoon', methods=['GET'], strict_slashes=False)
@token_required('user')
def coming_soon():
    """ These renders a page for all services that are currently not available"""
    return render_template('coming_soon.html')


# ADMIN DASHBOARD
@main.route('/admin_dashboard', methods=['GET'], strict_slashes=False)
@token_required('admin')
def admin_dashboard():
    """ Admin dashboard where admins can verify business registrations """
    unverified_businesses = storage.get_unverified_businesses()
    return render_template('admin_services.html', unverified_businesses=unverified_businesses)

@main.route('/pending_approval', methods=['GET'], strict_slashes=False)
@token_required('admin')
def pending_approval():
    """ Admin dashboard where admins can verify business registrations """
    return render_template('pending_approval.html')


# business details
@main.route('/business_details/<string:business_id>', methods=['GET', 'POST'], strict_slashes=False)
@token_required('admin')
def business_details(business_id=None):
    """ Admin dashboard where admins can view business details """
    if request.method == 'POST':
        action = request.form.get('action')  # Get the action (approve or reject)
        if action == 'approve':
            storage.approve_business(business_id)
            return redirect(url_for('main.admin_dashboard'))  # Redirect to admin dashboard
        elif action == 'reject':
            storage.reject_business(business_id)
            return redirect(url_for('main.admin_dashboard'))  # Redirect to admin dashboard

    business_details = storage.get_business_details(business_id)
    return render_template('business_details.html', business_details=business_details)

# approved businesses
@main.route('/approved_businesses', methods=['GET'], strict_slashes=False)
@token_required('admin')
def approved_businesses():
    """ Page to display approved businesses """
    approved_businesses = storage.get_approved_businesses()
    return render_template('approved_businesses.html', approved_businesses=approved_businesses)

# rejected businesses
@main.route('/rejected_businesses', methods=['GET'], strict_slashes=False)
@token_required('admin')
def rejected_businesses():
    """ Page to display rejected/unverfied businesses """
    rejected_businesses = storage.get_unverified_businesses() # Get unverified same as rejected businesses
    return render_template('rejected_businesses.html', rejected_businesses=rejected_businesses)

