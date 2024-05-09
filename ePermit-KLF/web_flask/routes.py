from flask import render_template, url_for, redirect
from web_flask import app, db, mail
from web_flask.forms import LoginForm, RequestPasswordForm, ResetPasswordForm
from models.user import User
from web_flask import Message


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


def create_mail(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='sendermailid', recipients=[user.email])
    msg.body = f'''To reset your password, visit on following link: {url_for('reset_token', token=token, _external=True)}
    
If you did not make this request just ignore this mail.'''
    mail.send(msg)


@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        create_mail(user)
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset request', form=form)


@app.route("/reset_request/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        return "Your password has been updated, now you can login with your new password."
    return render_template('reset_password.html', title='Reset Password', form=form)