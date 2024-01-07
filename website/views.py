from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# when navigated to views route the 'home' function will run

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)



