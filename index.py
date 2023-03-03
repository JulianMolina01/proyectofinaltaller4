from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123Password123',
    database = 'clinica'
)
@app.route('/templates/dashboard.html')
def dashboard():
    if 'nombre' in session:
        return render_template('/dashboard.html', nombre=session['nombre'])
    else:
        return redirect(url_for('login'))

@app.route('/templates/login.html', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM login WHERE usuario = %s AND password = %s", (email, password))
        usuario = mycursor.fetchone()
        print("======= %s", usuario)
        if usuario:
            session['nombre'] = usuario[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('/login.html', mensaje = 'Email o Contraseña incorrectos, intente de nuevo por favor.')
    else:
        return render_template('/login.html')
    
@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contra = request.form['password']
        repite_contra = request.form['password_dos']
        if contra== repite_contra:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM login WHERE usuario = %s", (email,))
            resultado = mycursor.fetchone()
            if resultado:
                # El registro ya existe, enviar un mensaje y redirigir al usuario
                return render_template('/registro.html', mensaje = 'El registro ya existe!')
            else:
                mycursor.execute("INSERT INTO login (usuario, password) VALUES (%s, %s)", (email, contra))
                mydb.commit()
                return render_template('/registro.html', mensaje = 'Cuenta creada con exito!')
        else:
            return render_template('/registro.html', mensaje = 'Las contraseñas no coinciden :(')
    else:
        return render_template('/registro.html')

@app.route('/')
def home():
    return render_template('/index.html')
@app.route('/templates/citas.html')
def citas():
    return render_template('/citas.html')
@app.route('/templates/servicios.html')
def servicios():
    return render_template('/servicios.html')
@app.route('/templates/pacientes.html')
def pacientes():
    return render_template('/pacientes.html')
@app.route('/templates/contacto.html')
def contacto():
    return render_template('/contacto.html')

if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')