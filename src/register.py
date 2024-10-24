# src/register.py

from connection import connect_postgresql  # Import the connection function
from flask import request, redirect, url_for

def register_client():
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']

    conn = connect_postgresql()  # Use the connection function from connection.py
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO clientes (nombre, cedula, correo, telefono)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, cedula, correo, telefono))
                conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

    return redirect(url_for('home'))
