from flask import Blueprint, render_template

views = Blueprint('views', __name__)

# when navigated to views route the 'home' function will run
@views.route('/')
def home():
    return render_template("home.html")



