from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from api import db 


#-------Database config-----
class Usuarios(db.Model):
    ClienteID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(45))
    Apellido = db.Column(db.String(45))
    Direccion = db.Column(db.String(100))
    ProductoID = db.Column(db.Integer(),db.ForeignKey('productos.ProductoID',ondelete='NO ACTION', onupdate='NO ACTION'))
    producto_id = db.relationship('Productos',foreign_keys=ProductoID, backref='usuarios')
    FechaPago = db.Column(db.DateTime)
    Password = db.Column(db.String(45))
    Matricula = db.Column(db.Integer())

class Productos(db.Model):
    ProductoID= db.Column(db.Integer,primary_key=True)
    Nombre = db.Column(db.String(45))
    Descripcion = db.Column(db.String(45))

class Facturas(db.Model):
    FacturaID = db.Column(db.Integer, primary_key=True)
    FechaPago = db.Column(db.DateTime, nullable=False)
    MetodoPago = db.Column(db.String(), nullable=False)
    Descripcion = db.Column(db.String(), nullable=False)
    ClienteID = db.Column(db.Integer(),db.ForeignKey('usuarios.ClienteID'))
    cliente_id = db.relationship('Usuarios',foreign_keys=ClienteID, backref='Facturas')
    ProductoID = db.Column(db.Integer(),db.ForeignKey('productos.ProductoID'))
    producto_id = db.relationship('Productos',foreign_keys=ProductoID, backref='Facturas')

class Admins(UserMixin, db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    User = db.Column(db.String(45))
    Password = db.Column(db.String(45))
    def get_id(self):
           return (self.AdminID)
