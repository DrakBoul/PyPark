from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Flash error messages to user if any input field is not sufficient   
        if len(email) < 4:
            flash('Email must be greater than 3 characters', category="error")
        elif len(firstName) < 2:
            flash('first name must be greater then 1 characters', category="error")
        elif password1 != password2:
            flash('Your passwords do not match, please check your spelling', category="error")
        elif len(password1) < 7:
            flash('Your password must be greater then 6 characters', category="error")
            
        else:
            flash("Account Created", category="success")
            pass
        

    return render_template("sign_up.html")