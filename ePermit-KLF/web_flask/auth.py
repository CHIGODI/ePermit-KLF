from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import storage
from flask_login import login_user, logout_user, login_required
from web_flask import auth


@auth.route('/login', methods=['GET','POST'])
def login():
    # login code goes here
    if request.method == 'POST':
        user_email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = storage.get_user_by_email(user_email)
        
        if user is None or not check_password_hash(user.password, password):
            flash('Wrong email or password.')
            return redirect(url_for('auth.login')) 
        else:
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
    return render_template('login.html')



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # code to validate and add user to database goes here
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = storage.get_user_by_email(email)

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.login'))

        new_user = User(email=email, first_name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        storage.new(new_user)
        storage.save()
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.landing'))