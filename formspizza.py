from wtforms import Form
from wtforms import StringField,widgets,RadioField,EmailField,IntegerField,SelectMultipleField
from wtforms import validators

def validate_at_least_one(form, field):
    if not field.data:
        raise validators.ValidationError('Selecciona al menos un ingrediente')
class PizzaForm(Form):
    idP=IntegerField('idP')
    tamanio=RadioField('Seleciona el tamaño', 
                       choices=[(40 ,'chica $40'), (80, 'Mediana $80'), (120, 'Grande $120')])

    ingredientes = SelectMultipleField('Selecciona los ingredientes', choices=[
        ('jamon', 'Jamón $10'),
        ('pina', 'Piña $10'),
        ('champinones', 'Champiñones $10')
    ], validators=[validate_at_least_one], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    numeropizza = IntegerField('numero de pizzas', [
    validators.NumberRange(min=1, max=15, message='ingresa un número de pizzas válido')
    ])


    
class clienteForm(Form):
    idC=IntegerField('idC')
    
    nombreCompleto=StringField('Nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=15,message='ingresa nombre valido')
    ])
    direccion=StringField('direcion',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=40,message='ingresa nombre valido')
    ])
    telefono = StringField('telefono', validators=[
    validators.DataRequired(message='Ingresa un teléfono válido'),
    validators.length(min=5, max=15, message='Ingresa un teléfono válido con longitud entre 5 y 15 caracteres')
    ])


