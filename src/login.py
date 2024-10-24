from flask import flash, redirect, url_for, session
from connection import connect_postgresql  # Import the connection function
import base64

def login_user(form_data):
    cedula = form_data['cedula']
    correo = form_data['correo']
    
    # Connect to PostgreSQL to verify credentials
    connection = connect_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.id_cliente, m.saldo, c.qr_code FROM clientes c
                LEFT JOIN monedero m ON c.id_cliente = m.id_cliente
                WHERE c.cedula = %s AND c.correo = %s
            """, (cedula, correo))
            client = cursor.fetchone()
            
            if client:  # If credentials match, set session
                session['logged_in'] = True
                session['id_cliente'] = client[0]  # Set the id_cliente in session
                session['saldo'] = client[1]  # Assuming the second column is saldo
                
                # Encode QR code as base64 and store in session
                qr_code_binary = client[2]  # This is a memoryview object
                if qr_code_binary:
                    session['qr_code'] = base64.b64encode(qr_code_binary).decode('utf-8')  # Convert to base64 string
                else:
                    session['qr_code'] = None
                
                return redirect(url_for('home', message="Login successful!"))
            else:
                flash("Invalid credentials. Please try again.")
        except Exception as error:
            flash(f"Error during login: {error}")
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('login'))  # Redirect back to login if connection fails
