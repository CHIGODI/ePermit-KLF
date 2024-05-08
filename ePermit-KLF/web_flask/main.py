from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def landing():
    return render_template('landing_page.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('dashboard.html', name=current_user.first_name)