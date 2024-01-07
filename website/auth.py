from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.", category="error")
        else: 
            flash("Email does not exist", category="error")


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        UID = request.form.get('UID')

        user = User.query.filter_by(email=email).first()
        # Flash error messages to user if any input field is not sufficient
        if user:
            flash('Email already exists', category="error")   
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category="error")
        elif len(first_name) < 2:
            flash('first name must be greater then 1 characters', category="error")
        elif password1 != password2:
            flash('Your passwords do not match, please check your spelling', category="error")
        elif len(password1) < 7:
            flash('Your password must be greater then 6 characters', category="error")
        else:
            new_User = User(email=email, first_name=first_name, password=generate_password_hash(
                password1), UID=UID)
            db.session.add(new_User)
            db.session.commit()
            print(UID)
            flash("Account Created", category="success")
            login_user(new_User)

            return redirect(url_for('views.home'))

            
        

    return render_template("sign_up.html", user=current_user)