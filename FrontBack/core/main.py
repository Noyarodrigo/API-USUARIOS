from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import requests, json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    token_cookie = request.cookies.get('access_token')
    token_dict = {'access_token_cookie': token_cookie}
    r = requests.get('http://api:6000/user/15',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('profile.html', email=response['username']['AdminID'])

