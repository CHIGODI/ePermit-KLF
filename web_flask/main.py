#!/usr/bin/env python3
""" Main module contains routes to main pages of the Flask app. """

from flask import Blueprint, render_template, request, flash, g, redirect, url_for
from models import storage
from models.category import Category
from models.permit import Permit
from models.business import Business
from web_flask import main
from . import token_required
import uuid

cache_id = uuid.uuid4()

@main.route('/', methods=['GET'], strict_slashes=False)
def landing():
    return render_template('landing_page.html', cache_id=cache_id)


@main.route('/dashboard', methods=['GET'], strict_slashes=False)
@token_required('user')
def dashboard():
    """ User dashboard where normal users can register businesses """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    return render_template('services.html', businesses=businesses,
                           current_user=current_user,
                           cache_id=cache_id)

@main.route('/mybusinesses', methods=['GET'], strict_slashes=False)
@token_required('user')
def mybusinesses():
    """ user businesses """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    permits = storage.all(Permit).values()
    return render_template('my_businesses.html',
                           businesses=businesses,
                           permits=permits,
                           current_user=current_user,
                           cache_id=cache_id)

@main.route('/myprofile', methods=['GET'], strict_slashes=False)
@token_required('user')
def myprofile():
    """ user profile """
    current_user = g.get('current_user')
    return render_template('my_profile.html', current_user=current_user,
                           cache_id=cache_id)


@main.route('/mypermits', methods=['GET'], strict_slashes=False)
@token_required('user')
def mypermits():
    """ user permits """
    current_user = g.get('current_user')
    businesses = current_user.businesses
    business_ids = [business.id for business in businesses]
    permits = [p for p in storage.all(Permit).values() if p.business_id in business_ids]

    print(permits)
    return render_template('my_permits.html', permits=permits,
                           current_user=current_user,
                           cache_id=cache_id)


@main.route('/comingsoon', methods=['GET'], strict_slashes=False)
@token_required('user')
def coming_soon():
    """ These renders a page for all services that are currently not available"""
    current_user = g.get('current_user')
    return render_template('coming_soon.html',
                           current_user=current_user,
                           cache_id=cache_id)


# ADMIN DASHBOARD 
@main.route('/adminprofile', methods=['GET'], strict_slashes=False)
@token_required('admin')
def admin_profile():
    """ admin profile """
    current_user = g.get('current_user')
    return render_template('admin_profile.html', current_user=current_user,
                           cache_id=cache_id)
#Render unverified businesses
@main.route('/admin_dashboard', methods=['GET'], strict_slashes=False)
@token_required('admin')
def admin_dashboard():
    """ Admin dashboard where admins can verify business registrations """
    current_user = g.get('current_user')
    unverified_businesses = storage.get_unverified_businesses()
    return render_template('pending_approval.html', unverified_businesses=unverified_businesses,
                           current_user=current_user,
                           cache_id=cache_id)


# business details to either reject or approve
@main.route('/business_details/<string:business_id>', methods=['GET', 'POST'], strict_slashes=False)
@token_required('admin')
def business_details(business_id=None):
    """ Admin dashboard where admins can view business details """
    current_user = g.get('current_user')
    if request.method == 'POST':
        action = request.form.get('action')  
        if action == 'approve':
            storage.approve_business(business_id)
            return redirect(url_for('main.admin_dashboard'))  
        elif action == 'reject':
            storage.reject_business(business_id)
            return redirect(url_for('main.admin_dashboard'))  

    business_details = storage.get_business_details(business_id)
    return render_template('business_details.html', business_details=business_details,
                           current_user=current_user,
                           cache_id=cache_id)

# approved businesses
@main.route('/approved_businesses', methods=['GET'], strict_slashes=False)
@token_required('admin')
def approved_businesses():
    """ Page to display approved businesses """
    current_user = g.get('current_user')
    approved_businesses = storage.get_approved_businesses()
    return render_template('approved.html', approved_businesses=approved_businesses,
                           current_user=current_user,
                           cache_id=cache_id)

# rejected businesses
@main.route('/rejected_businesses', methods=['GET'], strict_slashes=False)
@token_required('admin')
def rejected_businesses():
    """ Page to display rejected/unverfied businesses """
    current_user = g.get('current_user')
    rejected_businesses = storage.get_rejected_businesses() 
    return render_template('rejected.html', rejected_businesses=rejected_businesses, current_user=current_user, cache_id=cache_id)



@main.route('/business_view/<string:business_id>', methods=['GET'], strict_slashes=False)
@token_required('admin')
def business_view(business_id=None):
    """ Admin view for business details without action buttons """
    current_user = g.get('current_user')
    business_details = storage.get_business_details(business_id)
    if business_details.verified is True:
        return render_template('approved_businesses.html', business_details=business_details, current_user=current_user)
    else:
        return render_template('rejected_businesses.html', business_details=business_details, current_user=current_user)

