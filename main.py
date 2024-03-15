from flask import Flask,render_template,request,flash,Response,g,jsonify,redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import redirect
import forms
import formspizza
from models import db
from datetime import datetime
from sqlalchemy import func
from config import DevelopmentConfig
from models import Empleado
from models import Cliente
from models import Pizza
from models import Venta
from config import DevelopmentConfig2 
import calendar
import locale
import formspizza as fp
from datetime import datetime
from flask import get_flashed_messages
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
idPizza=0
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
datos = []
cliente=[]

#nombre correo telefono, direcion, sueldo

@app.route("/index",methods=["GET","POST"])
def index():
    emp_form=forms.UsarForm(request.form)
    if request.method=='POST':
         emp=Empleado(nombre=emp_form.nombre.data,
                      telefono=emp_form.telefono.data,
                      direccion=emp_form.direccion.data,
                      sueldo=emp_form.sueldo.data,
                      correo=emp_form.email.data)
         #para mandar los datos seran por seciones 
         db.session.add(emp)
         db.session.commit()
         

    return render_template("index.html",form=emp_form)


@app.route("/ABC_Completo",methods=["GET","POST"])
def ABC_Completo():
    emp_form=forms.UsarForm(request.form)
    #para hacer una consulta
    empleado=Empleado.query.all()
    return render_template("ABC_Completo.html",empleados=empleado)

@app.route("/alumnos",methods=["GET","POST"])
def alum():
    
    alum_form=forms.UsarForm(request.form)
    nom=''
    apa=''
    ama=''
    mensaje=''
    #para validar que los campos no tengan un error se agrega el validate 
    if request.method=='POST' and alum_form.validate():
        nom=alum_form.nombre.data
        apa=alum_form.apaterno.data
        ama=alum_form.amaterno.data
        mensaje='Bienvenido {}'.format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom))
        print("Apellido Paterno: {}".format(apa))
        print("Apellido Materno: {}".format(ama))
    return render_template("alumnos.html",form=alum_form,nom=nom,apa=apa,ama=ama)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/eliminar",methods=["GET","POST"])
def eliminar():
    emp_form=forms.UsarForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        #aqui pasamos la condicion que queremos buscar 
        emp1=db.session.query(Empleado).filter(Empleado.id==id).first()
        emp_form.id.data=request.args.get('id')
        emp_form.nombre.data=emp1.nombre
        emp_form.telefono.data=emp1.telefono
        emp_form.email.data=emp1.correo
        emp_form.sueldo.data=emp1.sueldo
        emp_form.direccion.data=emp1.direccion
    if request.method=='POST':
        id=emp_form.id.data
        alum=Empleado.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template('eliminar.html',form=emp_form)



@app.route("/modificar",methods=["GET","POST"])
def modificar():
    emp_form=forms.UsarForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        #aqui pasamos la condicion que queremos buscar 
        emp1=db.session.query(Empleado).filter(Empleado.id==id).first()
        emp_form.id.data=request.args.get('id')
        emp_form.nombre.data=emp1.nombre
        emp_form.telefono.data=emp1.telefono
        emp_form.email.data=emp1.correo
        emp_form.sueldo.data=emp1.sueldo
        emp_form.direccion.data=emp1.direccion
    if request.method=='POST':
        id=emp_form.id.data
        emp1=db.session.query(Empleado).filter(Empleado.id==id).first()
        emp1.nombre=emp_form.nombre.data
        emp1.telefono=emp_form.telefono.data 
        emp1.correo=emp_form.email.data
        emp1.direccion=emp_form.direccion.data
        db.session.add(emp1)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template('modificar.html',form=emp_form)

@app.route("/pizzaA",methods=["GET","POST"])
def pizzaA():
  
    pizza_form=formspizza.PizzaForm(request.form)
    pizza_form2=formspizza.clienteForm(request.form)
   
    return render_template("vistaPizzaAgregar.html",form=pizza_form2,form2=pizza_form)


@app.route("/agregarP", methods=["GET", "POST"])
def agregarp():
    global datos
    global cliente
    message=''
    clienteFor = fp.clienteForm(request.form)
    pizzaform = fp.PizzaForm(request.form)
    nombreCompleto = ''
    direccion = ''
    telefono = ''
    fecha =''
    fecha_compra=''
    idc=''
    if request.method == "POST"and  clienteFor.validate() :

        ingredientes = []
        form_data = request.form.to_dict()
        print('repuesta',form_data)
        if "registrar" in request.form and pizzaform.validate():
            nombreCompleto = clienteFor.nombreCompleto.data
            direccion = clienteFor.direccion.data
            telefono = clienteFor.telefono.data
            fecha = str(clienteFor.fecha.data)
            print(pizzaform.tamanio.data)
            tamanio = int(pizzaform.tamanio.data)
            ingredientes = pizzaform.ingredientes.data
            numeropizza = int(pizzaform.numeropizza.data)
            ing = len(ingredientes)
            subtotal = (tamanio + (ing * 10)) * numeropizza

            if tamanio == 40:
                tamanio = 'Chica'
            elif tamanio == 80:
                tamanio = 'Mediana'
            else:
                tamanio = 'Grande'
            if clienteFor.idC.data.strip() and clienteFor.idC.data.isdigit():
                idc=int(clienteFor.idC.data)
                nueva_pizza = {
                    'tamanio': tamanio,
                'ingredientes': ingredientes,
                'numeropizza': numeropizza,
                'subtotal': subtotal
                    }
                if 0 <= idc < len(datos):
                        datos[idc] = nueva_pizza
                t = sum(pizza['subtotal'] for pizza in datos)
                message =f'El total de la cantidad es: {t}. ¿Estás de acuerdo?'
                clienteFor.idC.data=''
            else:
                pizza = {
                'tamanio': tamanio,
                'ingredientes': ingredientes,
                'numeropizza': numeropizza,
                'subtotal': subtotal
                }
                datos.append(pizza)
                print('pizzas',datos)
                cliente_existente = next((c for c in cliente if c['nombreCompleto'] == nombreCompleto), None)
                if not cliente_existente:
                    c = {
                    'nombreCompleto': nombreCompleto,
                    'direccion': direccion,
                    'telefono': telefono,
                    'fecha': fecha
                }
                    cliente.append(c)
                    print('cliente ',cliente)
                t = sum(pizza['subtotal'] for pizza in datos)
                message =f'El total de la cantidad es: {t}. ¿Estás de acuerdo?'

          

          
        elif "Botonsi" in request.form:
            nombreCompleto = clienteFor.nombreCompleto.data
            direccion = clienteFor.direccion.data
            telefono = clienteFor.telefono.data
            fecha = clienteFor.fecha.data
            t = sum(pizza['subtotal'] for pizza in datos)

            cl = Cliente(nombre_completo=nombreCompleto,
                         telefono=telefono,
                         direccion=direccion,
                         fecha_compra=fecha)
            db.session.add(cl)
            db.session.commit()
            id_cliente = cl.idCliente
            for pizza_data in datos:
                tamanio = pizza_data['tamanio']
                ingredientes = ', '.join(pizza_data['ingredientes'])
                numPizza = pizza_data['numeropizza']
                subtotal = pizza_data['subtotal']
                fecha_compra = fecha

                # Crear una instancia del modelo Pizza y asignar el ID del cliente
                pizza_model = Pizza(tamano=tamanio, ingredientes=ingredientes, numero_pizza=numPizza,
                                    subtotal=subtotal, idCliente=id_cliente)

                # Agregar la pizza a la base de datos
                db.session.add(pizza_model)
                db.session.commit()

            venta = Venta(idCliente=id_cliente, total=t, fecha_venta=fecha_compra)
            db.session.add(venta)
            db.session.commit()
            datos=[]
            cliente=[]
            clienteFor.nombreCompleto.data = ''
            clienteFor.direccion.data = ''
            clienteFor.telefono.data = ''
            clienteFor.fecha.data = None
            pizzaform.tamanio.data = None
            pizzaform.ingredientes.data = []
            pizzaform.numeropizza.data = None
            message ='Registro exitos'
        elif "Botonno" in request.form:
            t = sum(pizza['subtotal'] for pizza in datos)
            message =f'El total de la cantidad es: {t}. ¿Estás de acuerdo?'
    return render_template('vistaPizzaAgregar.html', form=clienteFor, form2=pizzaform, pizzas=datos,message=message)









@app.route("/tabla",methods=["POST"])
def tabla():
    dia=request.form.get('dia')
    resultados = (
    db.session.query(
        Cliente.nombre_completo,
        func.sum(Venta.total).label('total'),
        func.dayname(Venta.fecha_venta).label('day_of_week')
    )
    .join(Venta, Venta.idCliente == Cliente.idCliente)
    .filter(func.dayname(Venta.fecha_venta) == dia)
    .group_by(Cliente.nombre_completo, func.dayname(Venta.fecha_venta))
    .all()
) 
    dias_en_ingles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_en_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    indice = dias_en_ingles.index(dia .capitalize())
    d=dias_en_espanol[indice]

    # Calcular la suma de los totales
    suma_totales = str(sum(resultado.total for resultado in resultados))

    pizza_form=formspizza.PizzaForm(request.form)
    pizza_form2=formspizza.clienteForm(request.form)

    return render_template("vistaPizzaAgregar.html",form=pizza_form2,form2=pizza_form,resultados=resultados,suma=suma_totales,mes=d)

@app.route("/tabla2",methods=["GET","POST"])
def tabla2():
    mes=request.form.get('mes')
    resultados = (
    db.session.query(
        Cliente.nombre_completo,
        func.sum(Venta.total).label('total'),
        func.month(Venta.fecha_venta).label('month_of_year')
    )
    .join(Venta, Venta.idCliente == Cliente.idCliente)
    .filter(func.month(Venta.fecha_venta) == mes)
    .group_by(Cliente.nombre_completo, func.month(Venta.fecha_venta))
    .all()
)
    nombre_mes = calendar.month_name[int(mes)]

    suma_totales = str(sum(resultado.total for resultado in resultados))

    pizza_form=formspizza.PizzaForm(request.form)
    pizza_form2=formspizza.clienteForm(request.form)

    return render_template("vistaPizzaAgregar.html",form=pizza_form2,form2=pizza_form,resultados=resultados,suma=suma_totales,mes=nombre_mes)


@app.route('/eliminarp', methods=['GET'])
def eliminar_pizza():
    clienteFor=fp.clienteForm(request.form)
    pizzaform=fp.PizzaForm(request.form)
    pizza_id = int(request.args.get('pizza_id'))
    if 0 <= pizza_id < len(datos):
        del datos[pizza_id]
    t = sum(pizza['subtotal'] for pizza in datos)
    message =f'El total de la cantidad es: {t}. ¿Estás de acuerdo?'
    if cliente:    
        fecha = datetime.strptime(cliente[0]['fecha'], '%Y-%m-%d') 
        clienteFor.nombreCompleto.data = cliente[0]['nombreCompleto']
        clienteFor.direccion.data = cliente[0]['direccion']
        clienteFor.telefono.data = cliente[0]['telefono']
        clienteFor.fecha.data = fecha.date() 
    else:
        print("La lista cliente está vacía")

    return render_template('vistaPizzaAgregar.html', form=clienteFor,form2=pizzaform,pizzas=datos,message=message)


from datetime import datetime

@app.route('/modificarp', methods=['GET'])
def modificar_pizza():
    clienteFor = fp.clienteForm(request.form)
    pizzaform = fp.PizzaForm(request.form)
    pizza_id = int(request.args.get('pizza_id'))
    t=''
    if 0 <= pizza_id < len(datos):
        pizza_seleccionada = datos[pizza_id]
        if pizza_seleccionada['tamanio'] == 'Chica':
            t = '40'
        elif pizza_seleccionada['tamanio'] == 'Mediana':
            t = '80'
        elif pizza_seleccionada['tamanio'] == 'Grande':
            t = '120'
        
        pizzaform.tamanio.data = t
        pizzaform.ingredientes.data = pizza_seleccionada['ingredientes']
        pizzaform.numeropizza.data = pizza_seleccionada['numeropizza']
           
    else:
        # Si el ID de la pizza no es válido, regresar un mensaje de error
        return "El ID de la pizza seleccionada no es válido."
   
    if cliente:
        fecha = datetime.strptime(cliente[0]['fecha'], '%Y-%m-%d')
        clienteFor.nombreCompleto.data = cliente[0]['nombreCompleto']
        clienteFor.direccion.data = cliente[0]['direccion']
        clienteFor.telefono.data = cliente[0]['telefono']
        clienteFor.fecha.data = fecha.date()
        clienteFor.idC.data=str(pizza_id)
    else:
        print("La lista cliente está vacía")
        
    t = sum(pizza['subtotal'] for pizza in datos)
    message =f'El total de la cantidad es: {t}. ¿Estás de acuerdo?'
    return render_template('vistaPizzaAgregar.html', form=clienteFor, form2=pizzaform, pizzas=datos, message=message)
    

#especificar el metodo que va a arrancar la aplicacion 
if __name__=="__main__":
    #csrf.init_app(app)
    db.init_app(app)
   # with app.app_context():
   #     db.create_all()
    app.run()    


    