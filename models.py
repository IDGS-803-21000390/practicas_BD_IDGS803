from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import datetime

db=SQLAlchemy()
#nombre correo telefono, direcion, sueldo

class Empleado(db.Model):
    _tablename_='empleados'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    correo=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    direccion=db.Column(db.String(100))
    sueldo=db.Column(db.Integer)
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)


class Pizza(db.Model):
    __tablename__ = 'detalle_pizza'
    idPizza = db.Column(db.Integer,primary_key=True)
    tamanio = db.Column(db.String(10))
    ingredientes = db.Column(db.String(20))
    numero_pizza = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)
    idCliente=db.Column(db.Integer)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer,primary_key=True)
    nombre_completo = db.Column(db.String(100))
    direcion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_compra =db.Column(db.Date)

class Venta(db.Model):
    __tablename__ = 'venta'
    idVenta = db.Column(db.Integer,primary_key=True)
    idCliente = db.Column(db.Integer)
    total = db.Column(db.Integer)
    fecha_venta = db.Column(db.Date)