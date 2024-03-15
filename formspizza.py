from wtforms import Form
from wtforms import StringField,widgets,RadioField,EmailField,IntegerField,SelectMultipleField,DateField
from wtforms import validators

def validate_at_least_one(form, field):
    if not field.data:
        raise validators.ValidationError('Selecciona al menos un ingrediente')
class PizzaForm(Form):
    idP=IntegerField('idP')
    tamanio=RadioField('Seleciona el tamaño', 
                       choices=[(40 ,'Chica $40'), (80, 'Mediana $80'), (120, 'Grande $120')])

    ingredientes = SelectMultipleField('Selecciona los ingredientes', choices=[
        ('jamon', 'Jamón $10'),
        ('pina', 'Piña $10'),
        ('champinones', 'Champiñones $10')
    ], validators=[validate_at_least_one], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    numeropizza = IntegerField('numero de pizzas', [
        validators.InputRequired(message='Este campo es obligatorio'),
        validators.NumberRange(min=1, max=10000, message='ingresa un número de pizzas válido')
    ])


    
class clienteForm(Form):
    idC=StringField('',render_kw={"type": "hidden"})
    
    nombreCompleto=StringField('Nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=5, max=15,message='ingresa nombre valido')
    ])
    direccion=StringField('direcion',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=5, max=40,message='ingresa nombre valido')
    ])
    telefono = StringField('telefono', validators=[
    validators.DataRequired(message='Ingresa un teléfono válido'),
    validators.length(min=5, max=15, message='Ingresa un teléfono válido con longitud entre 5 y 15 caracteres')
    ])
    fecha = DateField('Fecha', validators=[validators.DataRequired(message='Por favor, ingresa una fecha')])


