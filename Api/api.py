import os
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from sqlalchemy.orm import sessionmaker

#-------  API usuario -------
#buscar todos los usuarios
@app.route('/user',methods=['GET'])
@login_required
def get_all_users():
    users = Usuarios.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['ID'] = user.ClienteID
        user_data['Nombre'] = user.Nombre
        user_data['Apellido'] = user.Apellido
        user_data['Direccion'] = user.Direccion
        output.append(user_data)

    return jsonify({'usuarios' : output})

#buscar un usuario
@app.route('/user/<id>',methods=['GET'])
def get_one_user(id):
    user = db.session.query(Usuarios.ClienteID, Usuarios.Nombre,Usuarios.Apellido, Usuarios.Matricula,Productos.Descripcion,Usuarios.Direccion,Usuarios.FechaPago)\
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
    user_data['Producto'] = user.Descripcion
    user_data['Matricula'] = user.Matricula
    user_data['FechaPago'] = user.FechaPago
    return jsonify({'user':user_data})

#crear usuario
@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Usuarios(Nombre= data['Nombre'], Apellido= data['Apellido'], Direccion= data['Direccion'],ProductoID=data['Producto'], Password= data['Apellido'],Matricula= data['Matricula'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'cliente agregado'})

#modificar usuario
@app.route('/user/<id>',methods=['PUT'])
def alter_user(id):
    user = Usuarios.query.filter_by(ClienteID=id).first()
    if not user:
        return jsonify({'message':'No existe el usuario'})
    args = request.args
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
def get_all_bills():
    #bills = Facturas.query.all()

    bills = db.session.query(Facturas.FacturaID, Usuarios.ClienteID, Usuarios.Nombre, Usuarios.Apellido, Facturas.Descripcion,Facturas.MetodoPago,Facturas.FechaPago)\
            .filter(Facturas.ClienteID == Usuarios.ClienteID)\
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
        bill_data['FechaPago'] = bill.FechaPago
        output.append(bill_data)
    return jsonify({'bills' : output})

#buscar una factura
@app.route('/factura/<id>',methods=['GET'])
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
    bill_data['FechaPago'] = bill.FechaPago
    return jsonify({'bill':bill_data})

#crear factura
@app.route('/factura',methods=['POST'])
def create_bill():
    data = request.get_json()
    #check if user exist
    user = Usuarios.query.filter_by(ClienteID=data['Cliente']).first()
    if not user:
        return jsonify({'message':'No existe el usuario'})

    new_bill = Facturas(ClienteID= data['Cliente'], Descripcion= data['Descripcion'], MetodoPago= data['MetodoPago'], FechaPago=data['FechaPago'])
    db.session.add(new_bill)
    user.FechaPago = data['FechaPago']
    db.session.commit()

    return jsonify({'message':'factura agregada'})

#modificar factura
@app.route('/factura/<id>',methods=['PUT'])
def alter_bill(id):
    bill = Facturas.query.filter_by(FacturaID=id).first()
    if not bill:
        return jsonify({'message':'No existe la factura'})
    args = request.args
    if 'Cliente' in args:
        bill.ClienteID = args['Cliente']
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
def delete_facturas(id):
    bill = Facturas.query.filter_by(FacturaID=id).first()
    if not bill:
        return jsonify({'message':'No existe la factura'})
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'message':'Factura eliminada'})


@app.route('/')
def hello():
    return "<h1>Hello mundo</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'),debug=True)
