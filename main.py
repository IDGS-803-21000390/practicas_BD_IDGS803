from flask import Flask,render_template,request,flash,Response,g
from flask_wtf.csrf import CSRFProtect
from flask import redirect
import forms
from models import db


from config import DevelopmentConfig
from models import Empleado

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
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



#especificar el metodo que va a arrancar la aplicacion 
if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()    


    