from flask import Blueprint

views = Blueprint('views', __name__)

# when navigated to views route the 'home' function will run
@views.route('/')
def home():
    return "<h1>Test</h1>"



