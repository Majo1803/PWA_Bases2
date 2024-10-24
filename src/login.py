from flask import flash, redirect, url_for, session
from connection import connect_postgresql  # Import the connection function

def login_user(form_data):
    cedula = form_data['cedula']
    correo = form_data['correo']
    
    # Connect to PostgreSQL to verify credentials
    connection = connect_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.id_cliente, m.saldo FROM clientes c
                LEFT JOIN monedero m ON c.id_cliente = m.id_cliente
                WHERE c.cedula = %s AND c.correo = %s
            """, (cedula, correo))
            client = cursor.fetchone()
            
            if client:  # If credentials match, set session
                session['logged_in'] = True
                session['id_cliente'] = client[0]  # Set the id_cliente in session
                session['saldo'] = client[1]  # Assuming the second column is saldo
                return redirect(url_for('home', message="Login successful!"))
            else:
                flash("Invalid credentials. Please try again.")
        except Exception as error:
            flash(f"Error during login: {error}")
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('login'))  # Redirect back to login if connection fails
