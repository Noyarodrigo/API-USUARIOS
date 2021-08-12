from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import requests, json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/usuarios')
@login_required
def usuarios():
    token_dict = get_cookie()
    r = requests.get('http://api:6000/user',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('usuarios.html', usuarios=response['usuarios'])

@main.route('/servicios')
@login_required
def servicios():
    token_dict = get_cookie()
    r = requests.get('http://api:6000/user',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('usuarios.html', usuarios=response['usuarios'])

@main.route('/facturas')
@login_required
def facturas():
    token_dict = get_cookie()
    r = requests.get('http://api:6000/user',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('usuarios.html', email=response)

def get_cookie():
    token_cookie = request.cookies.get('access_token')
    token_dict = {'access_token_cookie': token_cookie}
    return token_dict
