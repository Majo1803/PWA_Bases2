import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from register import register_client
from login import login_user
from connection import connect_postgresql  # Import the connection function

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Set the secret key for sessions
app.secret_key = 'your_unique_secret_key_here'

def get_balance(cliente_id):
    """Function to get the balance from the monedero table for the given cliente_id."""
    connection = connect_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT saldo FROM monedero WHERE id_cliente = %s;", (cliente_id,))
            saldo = cursor.fetchone()
            return saldo[0] if saldo else None
        except Exception as error:
            flash(f"Error retrieving balance: {error}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None

def get_client_info(cliente_id):
    """Function to get the client's main information."""
    connection = connect_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre, cedula, correo, telefono FROM clientes WHERE id_cliente = %s;", (cliente_id,))
            client_info = cursor.fetchone()
            return client_info  # Return client info as a tuple
        except Exception as error:
            flash(f"Error retrieving client info: {error}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None

@app.route('/')
def home():
    message = request.args.get('message')
    balance = None  # Initialize balance variable
    client_info = None  # Initialize client_info variable

    if 'logged_in' in session:  # Check if the user is logged in
        balance = get_balance(session['id_cliente'])  # Get the balance for the logged-in user
        client_info = get_client_info(session['id_cliente'])  # Get the client info

    return render_template('index.html', message=message, balance=balance, client_info=client_info)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = register_client(request.form)
        if "successfully" in result:
            return redirect(url_for('home', message=result))
        return render_template('register.html', message=result)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_user(request.form)
    return render_template('login.html')

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True)
