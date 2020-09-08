# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))

                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)





from flask import Flask, render_template,url_for,redirect,request,flash
from flaskext.mysql import MySQL
from datetime import datetime



app= Flask(__name__)

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


@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['email']
        direccion = request.form['direccion']
        clave = request.form['password']
        now = datetime.now()
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO Persona (idrol, nombre, apellido, telefono, correo, direccion,FechaUnion,clave) VALUES (%s,%s,%s,%s, %s, %s,%s,%s)", (2,nombre,apellido,telefono,correo, direccion,now,clave))
        mysql.get_db().commit()
        return redirect(url_for('inicio'))

@app.route('/check',methods=['GET'])
def check_user():
    if request.method == 'GET':
        user = request.form['usuario']
        psw = request.form['psw']
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT correo FROM persona WHERE clave=%s AND correo=%s;",(psw,user))
        result = cursor.fetchone()
        if result:
            return redirect(url_for("inicio"))
        else:
            flash('no esta registrado')



if __name__ == "__main__":
    app.run(debug=True)