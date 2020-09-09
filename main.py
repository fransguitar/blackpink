from flask import Flask, render_template,url_for,redirect,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flaskext.mysql import MySQL
from datetime import datetime
from flask_login import LoginManager
#import json


app= Flask(__name__)

userg=0


#app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
#login_manager = LoginManager(app)

#Configuracion de conexion 
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] ='moni123.,'
app.config['MYSQL_DATABASE_DB'] = 'blackpinkfinal'

mysql= MySQL()
mysql.init_app(app)



@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/cart')
def cart():
    if userg == 0:
        return render_template('register.html')
    
    else:
        return render_template('cart.html')    

@app.route('/gopay')
def gopay():
    if userg == 0:
        return render_template('register.html')
    
    else:
        return render_template('payment.html')
        
    


@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/payment')
def payment():
    return render_template('payment.html') 

@app.route('/shop')
def shop():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM producto")
    datos=cursor.fetchall()
    return render_template('shop.html',productos =datos)

@app.route('/singleproduct/<id>')
def singleproduct(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT  id, nombre, substring(direccionimagen,17), idtipo, idtemporada, idproveedor, idtalla, cantidad, descripcion, preciocompra, precioventa FROM producto WHERE id = %s', (id))
    datos = cursor.fetchall()
    return render_template('single-product.html',singproc=datos)



@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['email']
        direccion = request.form['direccion']
        clave = request.form['password']
        user =request.form['usuario']
        now = datetime.now()
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO Persona (idrol, nombre, apellido, telefono, correo, direccion,FechaUnion,clave,usuario) VALUES (%s,%s,%s,%s, %s, %s,%s,%s,%s)", (2,nombre,apellido,telefono,correo, direccion,now,clave,user))
        mysql.get_db().commit()
        return redirect(url_for('inicio'))

@app.route('/check',methods=['POST'])
def check_user():
    if request.method == 'POST':
        user = request.form['usuario']
        psw = request.form['password']
        cursor = mysql.get_db().cursor()
        result=cursor.execute("SELECT correo FROM persona WHERE usuario=%s AND clave=%s;",(user,psw))
        if result == 0:
            return redirect(url_for('register'))
        else:
            global userg 
            cur=mysql.get_db().cursor()
            userg = cur.execute("SELECT id FROM persona WHERE usuario=%s AND clave=%s;",(user,psw))
            return redirect(url_for('inicio'))
            



if __name__ == "__main__":
    app.run(debug=True)