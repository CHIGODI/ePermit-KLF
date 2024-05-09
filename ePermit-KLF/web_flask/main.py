from flask import Blueprint, render_template
from flask_login import login_required, current_user
from web_flask import main

@main.route('/')
def landing():
    return render_template('landing_page.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('dashboard.html', name=current_user.first_name)

@main.route('/comingsoon')
def comingsoon():
    return render_template('coming_soon.html')