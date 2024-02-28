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