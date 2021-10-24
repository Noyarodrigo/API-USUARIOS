import os
from flask import Flask, request, jsonify, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity)
import json
from datetime import date, datetime
from cryptography.fernet import Fernet
import dateutil

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile('/app/src/config/config.txt')
jwt = JWTManager(app)

from models import *

#-------  API usuario -------
#buscar todos los usuarios
@app.route('/user',methods=['GET'])
@jwt_required()
def get_all_users():
    users = Usuarios.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['ID'] = user.ClienteID
        user_data['Nombre'] = user.Nombre
        user_data['Apellido'] = user.Apellido
        user_data['Direccion'] = user.Direccion
        try:
            user_data['FechaPago'] = user.FechaPago.strftime("%Y/%m/%d")
        except:
            user_data['FechaPago'] = user.FechaPago

        output.append(user_data)

    return jsonify({'usuarios' : output})

#buscar un usuario
@app.route('/user/<id>',methods=['GET'])
@jwt_required()
def get_one_user(id):
    user = db.session.query(Usuarios.ClienteID, Usuarios.Nombre,Usuarios.Apellido, Usuarios.Matricula,Productos.Nombre.label("Producto"),Usuarios.Direccion,Usuarios.FechaPago,Usuarios.Password)\
            .filter(Usuarios.ClienteID == id)\
            .filter(Usuarios.ProductoID == Productos.ProductoID)\
            .first()

    if not user:
        return jsonify({'message':'Usuario no encontrado'})

    user_data = {}
    user_data['ID'] = user.ClienteID
    user_data['Nombre'] = user.Nombre
    user_data['Apellido'] = user.Apellido
    user_data['Direccion'] = user.Direccion
    user_data['Producto'] = user.Producto
    user_data['Matricula'] = user.Matricula
    user_data['FechaPago'] = user.FechaPago.strftime("%Y/%m/%d")
    user_data['Password'] = user.Password
    return jsonify({'user':user_data})

#crear usuario
@app.route('/user',methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    new_user = Usuarios(Nombre= data['nombre'], Apellido= data['apellido'], Direccion= data['direccion'],ProductoID=data['producto'], Password= data['password'],Matricula= data['matricula'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'cliente agregado'})

#modificar usuario
@app.route('/user/<id>',methods=['PUT'])
@jwt_required()
def alter_user(id):
    user = Usuarios.query.filter_by(ClienteID=id).first()
    if not user:
        return jsonify({'message':'No existe el usuario'})
    args = request.get_json()
    if 'Nombre' in args:
        user.Nombre = args['Nombre']
    if 'Apellido' in args:
        user.Apellido = args['Apellido']
    if 'Direccion' in args:
        user.Direccion = args['Direccion']
    if 'ProductoID' in args:
        user.ProductoID = args['ProductoID']
    if 'FechaPago' in args:
        user.FechaPago = args['FechaPago']
    if 'Password' in args:
        user.Password = args['Password']
    if 'Matricula' in args:
        user.Matricula = args['Matricula']
    db.session.commit()

    return jsonify({'message':'Modificado correctamente'})

#eliminar usuario
@app.route('/user/<id>',methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = Usuarios.query.filter_by(ClienteID=id).first()
    if not user:
        return jsonify({'message':'No existe el usuario'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'Usuario eliminado'})

#-------  API pago/login -------
#buscar fecha pago
@app.route('/login',methods=['POST'])
@jwt_required()
def get_payment():
    data = request.get_json()

    user = Usuarios.query.filter_by(Matricula=data['Matricula']).first()

    if not user:
        return jsonify({'message':'No existe el usuario'})

    if 'Nombre' not in data or 'Apellido' not in data or 'Matricula' not in data:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if user.Nombre != data['Nombre'] or user.Apellido != data['Apellido']:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user_data = {}
    user_data['FechaPago'] = user.FechaPago
    user_data['Matricula'] = user.Matricula
    return jsonify({'user':user_data})

#-------  API factura -------
#buscar todas las factuas
@app.route('/factura',methods=['GET'])
@jwt_required()
def get_all_bills():
    #bills = Facturas.query.all()

    bills = db.session.query(Facturas.FacturaID, Usuarios.ClienteID, Usuarios.Nombre, Usuarios.Apellido, Facturas.Descripcion,Facturas.MetodoPago,Facturas.FechaPago,Facturas.Monto)\
            .filter(Facturas.ClienteID == Usuarios.ClienteID)\
            .order_by(Facturas.FechaPago.desc())\
            .all()
    output = []
    for bill in bills:
        bill_data = {}
        bill_data['ClienteID'] = bill.ClienteID
        bill_data['FacturaID'] = bill.FacturaID
        bill_data['Nombre'] = bill.Nombre
        bill_data['Apellido'] = bill.Apellido
        bill_data['Descripcion'] = bill.Descripcion
        bill_data['MetodoPago'] = bill.MetodoPago
        bill_data['FechaPago'] = bill.FechaPago.strftime("%Y/%m/%d")
        bill_data['Monto'] = bill.Monto
        output.append(bill_data)
    return jsonify({'bills' : output})

#buscar una factura
@app.route('/factura/<id>',methods=['GET'])
@jwt_required()
def get_one_bill(id):
    bill = db.session.query(Facturas.FacturaID, Usuarios.ClienteID, Usuarios.Nombre, Usuarios.Apellido, Facturas.Descripcion,Facturas.MetodoPago,Facturas.FechaPago)\
            .filter(Facturas.FacturaID == id)\
            .filter(Facturas.ClienteID == Usuarios.ClienteID)\
            .first()

    if not bill:
        return jsonify({'message':'Factura no encontrada'})

    bill_data = {}
    bill_data['ClienteID'] = bill.ClienteID
    bill_data['FacturaID'] = bill.FacturaID
    bill_data['Nombre'] = bill.Nombre
    bill_data['Apellido'] = bill.Apellido
    bill_data['Descripcion'] = bill.Descripcion
    bill_data['MetodoPago'] = bill.MetodoPago
    bill_data['FechaPago'] = bill.FechaPago.strftime("%Y/%m/%d")
    return jsonify({'bill':bill_data})

#crear factura
@app.route('/factura',methods=['POST'])
@jwt_required()
def create_bill():
    data = request.get_json()
    #check if user exist
    user = Usuarios.query.filter_by(ClienteID=data['id']).first()
    if not user:
        return jsonify({'message':'No existe el usuario'})

    monto_producto = db.session.query(Productos.Monto)\
            .filter(Productos.ProductoID == Usuarios.ProductoID)\
            .filter(Usuarios.ClienteID==data['id'])\
            .first()

    new_bill = Facturas(ClienteID= data['id'], Descripcion= data['descripcion'], MetodoPago= data['metodo'], FechaPago=data['fecha'], Monto = monto_producto[0])
    db.session.add(new_bill)
    user.FechaPago = data['fecha']
    db.session.commit()

    return jsonify({'message':'factura agregada'})

#modificar factura
@app.route('/factura/<id>',methods=['PUT'])
@jwt_required()
def alter_bill(id):
    bill = Facturas.query.filter_by(FacturaID=id).first()
    if not bill:
        return jsonify({'message':'No existe la factura'})
    args = request.get_json()
    #return args
    #if 'Cliente' in args:
    #    bill.ClienteID = args['Cliente']
    if 'Descripcion' in args:
        bill.Descripcion = args['Descripcion']
    if 'MetodoPago' in args:
        bill.MetodoPago = args['MetodoPago']
    if 'FechaPago' in args:
        bill.FechaPago = args['FechaPago']
    if 'Producto' in args:
        bill.ProductoID = args['Producto']
    db.session.commit()

    return jsonify({'message':'Factura modificada correctamente'})

#eliminar factura
@app.route('/factura/<id>',methods=['DELETE'])
@jwt_required()
def delete_facturas(id):
    bill = Facturas.query.filter_by(FacturaID=id).first()
    if not bill:
        return jsonify({'message':'No existe la factura'})
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'message':'Factura eliminada'})

#-------  API productos -------
#buscar todos los productos
@app.route('/product',methods=['GET'])
@jwt_required()
def get_all_products():
    products = Productos.query.all()

    output = []
    for product in products:
        product_data = {}
        product_data['ID'] = product.ProductoID
        product_data['Nombre'] = product.Nombre
        product_data['Descripcion'] = product.Descripcion
        product_data['Monto'] = product.Monto
        output.append(product_data)

    return jsonify({'productos' : output})

#buscar un producto
@app.route('/product/<id>',methods=['GET'])
@jwt_required()
def get_one_product(id):
    product = db.session.query(Productos.ProductoID, Productos.Nombre,Productos.Descripcion,Productos.Monto)\
            .filter(Productos.ProductoID == id)\
            .first()

    if not product:
        return jsonify({'message':'Producto no encontrado'})

    product_data = {}
    product_data['ID'] = product.ProductoID
    product_data['Nombre'] = product.Nombre
    product_data['Descripcion'] = product.Descripcion
    product_data['Monto'] = product.Monto
    return jsonify({'producto':product_data})

#crear Producto
@app.route('/product',methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = Productos(Nombre= data['Nombre'], Descripcion= data['Descripcion'],Monto = data['Monto'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message':'Producto agregado'})

#modificar Producto
@app.route('/product/<id>',methods=['PUT'])
@jwt_required()
def alter_product(id):
    product = Productos.query.filter_by(ProductoID=id).first()
    if not product:
        return jsonify({'message':'No existe el Producto'})
    args = request.get_json()
    if 'Nombre' in args:
        product.Nombre = args['Nombre']
    if 'Descripcion' in args:
        product.Descripcion = args['Descripcion']
    if 'Monto' in args:
        product.Monto = args['Monto']
    db.session.commit()

    return jsonify({'message':'Modificado correctamente'})

#eliminar Producto
@app.route('/product/<id>',methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Productos.query.filter_by(ProductoID=id).first()
    if not product:
        return jsonify({'message':'No existe el Producto'})
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message':'Producto eliminado'})

#-------- API login/app ------
@app.route('/app/login', methods=['POST'])
def login_app():
    key = app.config['API_KEY']
    fernet = Fernet(key)
    api_key = request.headers['api-key']
    return jsonify({'key':key , 'api_key':api_key})
    matricula = fernet.decrypt(api_key).decode()

    if not matricula:
        return jsonify({'message':'Error en la matricula'})

    user = Usuarios.query.filter_by(Matricula=matricula).first()

    a_month = dateutil.relativedelta.relativedelta(months=1)
    pay_date = dateutil.parser.parse(user.FechaPago).date()

    expiration = pay_date + a_month
    current = datetime.date(datetime.now())

    if current > expiration:
        return jsonify({'message':'Servicio no abonado'})

    return jsonify({'status':'True', 'matricula':user.Matricula})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'),debug=True)
