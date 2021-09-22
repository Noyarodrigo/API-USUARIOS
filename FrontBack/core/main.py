from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import requests, json

main = Blueprint('main', __name__)

#this is just a comment for testing ci v3

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

@main.route('/usuarios/handler',methods=['GET','POST'])
@login_required
def user_handler():
    #csrf posible implementacion
    #r = requests.get('http://api:6000/product',cookies=token_dict, headers=token_dict['csrf_access_token'])
    token_dict = get_cookie()
    if request.method == 'GET':
        arg_data = request.args
        if '_method' in arg_data and arg_data['_method'] == '_DELETE':
            r = requests.delete('http://api:6000/user/'+ arg_data['id'],cookies=token_dict)
            #response = json.loads(r.text)
            return redirect('/usuarios') 

        if '_method' in arg_data and arg_data['_method'] == '_UPDATE':
            r = requests.get('http://api:6000/product',cookies=token_dict)
            response = json.loads(r.text)
            names = []
            for el in response['productos']:
               names.append([el['Nombre'],el['ID']]) 

            r = requests.get('http://api:6000/user/'+ arg_data['id'],cookies=token_dict)
            response = json.loads(r.text)
            return render_template('alteruser.html',data=response['user'], productos = names)

        r = requests.get('http://api:6000/product',cookies=token_dict)
        response = json.loads(r.text)
        names = []
        for el in response['productos']:
           names.append([el['Nombre'],el['ID']]) 
        return render_template('newuser.html',productos=names)

    if request.method == 'POST':
        form_data = request.form
        if form_data['accion'] == 'Actualizar':
            r = requests.put('http://api:6000/user/'+form_data['id'],cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/usuarios') 

        if form_data['accion'] == 'Crear':
            r = requests.post('http://api:6000/user',cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/usuarios') 

@main.route('/servicios')
@login_required
def servicios():
    token_dict = get_cookie()
    r = requests.get('http://api:6000/product',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('productos.html', productos=response['productos'])

@main.route('/servicios/handler',methods=['GET','POST'])
@login_required
def servicios_handler():
    token_dict = get_cookie()
    if request.method == 'GET':
        arg_data = request.args
        if '_method' in arg_data and arg_data['_method'] == '_DELETE':
            r = requests.delete('http://api:6000/product/'+ arg_data['id'],cookies=token_dict)
            #response = json.loads(r.text)
            return redirect('/servicios') 

        if '_method' in arg_data and arg_data['_method'] == '_UPDATE':
            r = requests.get('http://api:6000/product/'+ arg_data['id'],cookies=token_dict)
            response = json.loads(r.text)
            return render_template('alterservice.html',data=response['producto'], id=arg_data['id'])

        r = requests.get('http://api:6000/product',cookies=token_dict)
        response = json.loads(r.text)
        return render_template('newservice.html')

    if request.method == 'POST':
        form_data = request.form
        if form_data['accion'] == 'Actualizar':
            r = requests.put('http://api:6000/product/'+form_data['id'],cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/servicios') 

        if form_data['accion'] == 'Crear':
            r = requests.post('http://api:6000/product',cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/servicios') 

@main.route('/facturas')
@login_required
def facturas():
    token_dict = get_cookie()
    r = requests.get('http://api:6000/factura',cookies=token_dict)
    response = json.loads(r.text)
    return render_template('facturas.html', bills=response['bills'])

@main.route('/facturas/handler',methods=['GET','POST'])
@login_required
def facturas_handler():
    token_dict = get_cookie()
    if request.method == 'GET':
        arg_data = request.args
        if '_method' in arg_data and arg_data['_method'] == '_DELETE':
            r = requests.delete('http://api:6000/factura/'+ arg_data['id'],cookies=token_dict)
            #response = json.loads(r.text)
            return redirect('/facturas') 

        if '_method' in arg_data and arg_data['_method'] == '_UPDATE':
            r = requests.get('http://api:6000/product',cookies=token_dict)
            response = json.loads(r.text)
            names = []
            for el in response['productos']:
               names.append([el['Nombre'],el['ID']]) 

            r = requests.get('http://api:6000/factura/'+ arg_data['id'],cookies=token_dict)
            response = json.loads(r.text)
            return render_template('alterbill.html',data=response['bill'], productos = names, id = arg_data['id'])

        return render_template('newbill.html', id = arg_data['id'])

    if request.method == 'POST':
        form_data = request.form
        if form_data['accion'] == 'Actualizar':
            r = requests.put('http://api:6000/factura/'+form_data['id'],cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/facturas') 

        if form_data['accion'] == 'Crear':
            r = requests.post('http://api:6000/factura',cookies=token_dict,json= form_data)
            response = json.loads(r.text)
            return redirect('/facturas') 

def get_cookie():
    token_cookie = request.cookies.get('access_token')
    #csrf_cookie = request.cookies.get('csrf_access_token')
    #token_dict = {'access_token_cookie': token_cookie,'csrf_access_token': csrf_cookie}
    token_dict = {'access_token_cookie': token_cookie}
    return token_dict
