from flask import Blueprint, render_template, request
from web_flask import main
from . import token_required

@main.route('/')
def landing():
    return render_template('landing_page.html')


@main.route('/dashboard')
@token_required
def dashboard():
    """ User dashboard where normal users can register businesses """
    return render_template('dashboard.html')


@main.route('/admin_dashboard')
@token_required
def admin_dashboard():
    """ Admin dashboard where admins can verify business registrations """
    return render_template('admin_dashboard.html')


@main.route('/comingsoon')
@token_required
def comingsoon():
    """ These renders a page for all services that are currently not available"""
    return render_template('coming_soon.html')