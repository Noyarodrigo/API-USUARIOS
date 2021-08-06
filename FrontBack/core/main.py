from flask import Blueprint, render_template
from flask_login import login_required, current_user
import requests, json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    r = requests.get('http://api:6000/user/15')
    response = json.loads(r.text)
    #return render_template('profile.html', email=current_user.User)
    return render_template('profile.html', email=response)
