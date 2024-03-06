from flask import Flask,render_template,request,flash,Response,g,jsonify
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
idPizza=0
app=Flask(__name__)
app.config.from_object(DevelopmentConfig2)
csrf=CSRFProtect()

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


@app.route("/tabla",methods=["GET","POST"])
def tabla():
    dia_button_clicked = True
    mes_button_clicked = False
    resultados = (
    db.session.query(
        Cliente.nombre_completo,
        func.sum(Venta.total).label('total'),
        func.day(Venta.fecha_venta).label('day_of_month')
    )
    .join(Venta, Venta.idCliente == Cliente.idCliente)
    .group_by(Cliente.nombre_completo, func.day(Venta.fecha_venta))
    .all()
)


    # Calcular la suma de los totales
    suma_totales = str(sum(resultado.total for resultado in resultados))

    pizza_form=formspizza.PizzaForm(request.form)
    pizza_form2=formspizza.clienteForm(request.form)

    return render_template("vistaPizzaAgregar.html",form=pizza_form2,form2=pizza_form,resultados=resultados,suma=suma_totales,dia_button_clicked=dia_button_clicked, mes_button_clicked=mes_button_clicked)

@app.route("/tabla2",methods=["GET","POST"])
def tabla2():
    dia_button_clicked = False
    mes_button_clicked = True
    resultados = (
    db.session.query(
        Cliente.nombre_completo,
        func.sum(Venta.total).label('total'),
        func.day(Venta.fecha_venta).label('month_of_year')
    )
    .join(Venta, Venta.idCliente == Cliente.idCliente)
    .group_by(Cliente.nombre_completo, func.day(Venta.fecha_venta))
    .all()
)


    # Calcular la suma de los totales
    suma_totales = str(sum(resultado.total for resultado in resultados))

    pizza_form=formspizza.PizzaForm(request.form)
    pizza_form2=formspizza.clienteForm(request.form)

    return render_template("vistaPizzaAgregar.html",form=pizza_form2,form2=pizza_form,resultados=resultados,suma=suma_totales,dia_button_clicked=dia_button_clicked, mes_button_clicked=mes_button_clicked)


@app.route('/vista',methods=["POST"])
def inicio():
    data = request.json
    NC = data.get('nombreCompleto')
    tel=data.get('telefono')
    di=data.get('direccion')
    pizzas=data.get('pizzas', [])
    t=data.get('total')
    fecha_compra = datetime.now().date()
    cl=Cliente(nombre_completo=NC,
                      telefono=tel,
                      direcion=di,
                      fecha_compra=fecha_compra)
         #para mandar los datos seran por seciones 
    db.session.add(cl)
    db.session.commit()
    id_cliente = cl.idCliente
    for pizza in pizzas:
        tamanio = pizza.get('tamanio')
        ingredientes = pizza.get('ingredientes')
        numPizza = pizza.get('numPizza')
        subtotal = pizza.get('subtotal')

    # Crear una instancia del modelo Pizza y asignar el ID del cliente
        pizza_model = Pizza(tamanio=tamanio, ingredientes=ingredientes, numero_pizza=numPizza, subtotal=subtotal, idCliente=id_cliente)

    # Agregar la pizza a la base de datos
        db.session.add(pizza_model)
        db.session.commit()

    venta=Venta(idCliente=id_cliente,total=t,fecha_venta=fecha_compra)
    db.session.add(venta)
    db.session.commit()    
    response = {"success": True, "message": "exitoso"}
    return jsonify(response)    

#especificar el metodo que va a arrancar la aplicacion 
if __name__=="__main__":
    #csrf.init_app(app)
    db.init_app(app)
   # with app.app_context():
   #     db.create_all()
    app.run()    


    