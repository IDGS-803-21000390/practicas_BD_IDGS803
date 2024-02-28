from wtforms import Form
from wtforms import StringField,SelectField,RadioField,EmailField,IntegerField
from wtforms import validators

#nombre correo telefono, direcion, sueldo
class UsarForm(Form):
    #para validar se genra una lista de validaciones, para que sea un dato requerido
    id=IntegerField('id')
    nombre=StringField('nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=10,message='ingresa nombre valido')
    ])
    telefono=StringField('telefono',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=15,message='ingresa nombre valido')
    ])
    direccion=StringField('direcion',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=30, max=40,message='ingresa nombre valido')
    ])
    sueldo=IntegerField('sueldo')
    email=EmailField('correo',[validators.Email(message='Ingresa un correo valido')])