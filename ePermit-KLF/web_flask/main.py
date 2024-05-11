from flask import Blueprint, render_template
from flask_login import login_required, current_user
from web_flask import main

@main.route('/')
def landing():
    return render_template('landing_page.html')

@main.route('/profile')
@login_required
def profile():
     if current_user.is_authenticated:
        user_id = current_user.id
        email = current_user.email
        print(email)
        return render_template('dashboard.html',
                               user_id=user_id,
                               email=email)
   
@main.route('/comingsoon')
def comingsoon():
    return render_template('coming_soon.html')