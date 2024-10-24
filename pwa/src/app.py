import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from register import register_client  # Import the register function
from login import login_user  # Import the login function

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Set the secret key for sessions
app.secret_key = 'your_unique_secret_key_here'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre = request.form.get('nombre')
    cedula = request.form.get('cedula')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')

    # Verificación de campos
    if not nombre or not cedula or not correo:
        message = "Por favor, complete todos los campos obligatorios."
        return render_template('index.html', message=message)
    
    #enviar los datos a la base de datos
    result = register_client(nombre, cedula, correo, telefono)
    

    # Si todo está bien, podrías redirigir al usuario a otra página o mostrar un mensaje de éxito
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_user(request.form)  # Call the login function from login.py
    return render_template('login.html')

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True)
