from flask import Flask, render_template, session, request, redirect , url_for ,flash 
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_script import Manager
import csv



# Clase genrada para que Iniciar sesion en la web
class Mi_Login(FlaskForm):
		usuario = StringField('Usuario:', validators=[DataRequired()])
		contraseña = PasswordField('Contraseña:', validators=[DataRequired()])
		submit = SubmitField('Ingresar')

# Clase generada para registrase como Usuarios
class Registro(FlaskForm):
    usuario = StringField('Usuario' , validators=[DataRequired()]) 
    clave0 = PasswordField('Contraseña',validators=[DataRequired()])
    clave1 = PasswordField(' Validar Contraseña',validators=[DataRequired()])
    submit = SubmitField('Registrar')   

# Clase generada para listar Consultas de testing de Base de Datos
class Consultas(FlaskForm):
    basetotal = StringField('basetotal')
    mejorescomptradores = StringField('mejorescomptradores')
    clientes = StringField('clientes')
    productosxclientes = StringField('Usuario' , validators=[DataRequired()])


class Cliente_Productos(FlaskForm):
    cliente = StringField('Cliente' , validators=[DataRequired()]) 
    submit = SubmitField('Listar')   

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)

# Seguridad de Contraseña Secreta
app.config['SECRET_KEY'] = "matiasrojas"
csrf = CSRFProtect(app)

#Inicio web, se define url default y url /index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('001_inicio.html', username=session['username'])
    return render_template('001_inicio.html')

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


# TestClientes por productos
@app.route('/clientesporproductos',methods=['GET' , 'POST'])
def clientesporproductos():
    test = Cliente_Productos()
    if test.validate_on_submit():
        return redirect('/productosvendidos')   
    return redirect('/basetotal')



# Se genera URL /Inicio donde el usuario podra validar sus credenciales y tener acceso a PANEL DE CONSULTAS en la web.
@app.route('/ingresar', methods=['GET', 'POST'])
def iniciodesesion():
    inicio = Mi_Login()
    if inicio.validate_on_submit():
        nombre_archivo = "csv"   
        with open(nombre_archivo) as archivo:
            archivo_csv = csv.reader(archivo)
            for linea in archivo_csv:
                valores = linea
                user = valores[0]
                con = valores[1]
                if user == inicio.usuario.data and con == inicio.contraseña.data:
                    session['username'] = inicio.usuario.data
                    return redirect('/basetotal')
            else:
                 flash('Usuario y/o Contrasña No Validos')               
    return render_template('01_ingresar.html', login=inicio)

# Se genera URL /registrar donde el usuario podra generar su usuario y contraseña de acceso a la web.
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    reg = Registro()
    if reg.validate_on_submit():
        if reg.clave0.data == reg.clave1.data:
            nombre_archivo = "csv" 
            with open('csv', 'a') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [reg.usuario.data, reg.clave1.data]
                archivo_csv.writerow(registro)
                flash('Registrado Correctamente')
                return redirect('/ingresar')
        else:
            flash('Error al validar Contraseña, No son iguales')
    return render_template('02_registrar.html', datos=reg)



# Se genera URL /cerrarsesion donde el usuario podra cerrar su sesion activa.
@app.route('/cerrarsesion')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect('/ingresar')
    else:
        return redirect('/ingresar')


# Se genera URL /basetotal donde usuario que inicior sesion podran listar la base de datos total.
@app.route('/basetotal',methods=['GET' , 'POST'])
def basetotal():
    nombre_archivo = 'informacion2' 
    if 'username' in session:   
        with open(nombre_archivo) as archivo:
            listar = csv.reader(archivo)
            return render_template('basetotal.html',listar=listar, username=session['username'])
    else:
        flash('Debe Iniciar Sesion para acceder a esta Informacion')
        return redirect('/ingresar')

# Se genera URL /clientes donde usuario que inicio sesion podran listar los clientes.
@app.route('/clientes',methods=['GET' , 'POST'])
def clientes():
    nombre_archivo = 'informacion2' 
    test = Cliente_Productos()
    if 'username' in session:    
        with open(nombre_archivo) as archivo:
            listar = csv.reader(archivo)
            return render_template('clientes.html',listar=listar, bus=test, username=session['username'])

# Se genera URL /productosvendidos donde usuario que inicio sesion podran listar los productos vendidos.
@app.route('/productosvendidos',methods=['GET' , 'POST'])
def productosvendidos():
        nombre_archivo = 'informacion2'     
        if 'username' in session:
            with open(nombre_archivo) as archivo:
                listar = csv.reader(archivo)
                return render_template('productosvendidos.html',listar=listar, username=session['username'])




# Se genera URL /basedatos donde verificara que hay usuario logeado para mostrar informacion.
@app.route('/basedatos')
def basedatos():
    if 'username' in session:
        return render_template('03_basededatos.html', username=session['username']) 
    else:
        flash('Debe Iniciar Sesion para acceder a esta Informacion')
        return redirect('/ingresar')

#test navbar base
@app.route('/test')
def navbar():
    return render_template('base.html')

#test consultas
@app.route('/consultas')
def gestionar():
        return render_template('basetotal.html')

#test tutorial
@app.route('/tutorial')
def tutorial():
        return render_template('tutorial.html')




if __name__ == "__main__":
    app.run(debug=True)
    manager.run()
