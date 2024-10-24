# src/register.py

from connection import connect_postgresql  # Import the connection function
import random

def register_client(form_data):
    # Extracting data from the form
    nombre = form_data['nombre']
    cedula = form_data['cedula']
    correo = form_data['correo']
    telefono = form_data.get('telefono', '')  # Default to empty string if not provided

    # Connect to PostgreSQL and insert the new client
    connection = connect_postgresql()  # Use the connection function
    if connection:
        try:
            cursor = connection.cursor()
            # Insert new client into the clientes table
            cursor.execute("""
                INSERT INTO clientes (nombre, cedula, correo, telefono)
                VALUES (%s, %s, %s, %s) RETURNING id_cliente;
            """, (nombre, cedula, correo, telefono))

            # Get the ID of the newly created client
            new_client_id = cursor.fetchone()[0]

            # Insert a new record into the monedero table with an initial saldo of 10,000
            cursor.execute("""
                INSERT INTO monedero (id_cliente, saldo)
                VALUES (%s, %s);
            """, (new_client_id, random.randint(20,100000)))

            # Commit the transaction
            connection.commit()
            return "Client registered successfully!"  # Return success message
        except Exception as error:
            return f"Error registering client: {str(error)}"  # Return error message
        finally:
            cursor.close()
            connection.close()  # Always close the connection
    else:
        return "Failed to connect to the database."  # Return connection error message
