# src/register.py

from connection import connect_postgresql  # Import the connection function

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
            cursor.execute("""
                INSERT INTO clientes (nombre, cedula, correo, telefono)
                VALUES (%s, %s, %s, %s);
            """, (nombre, cedula, correo, telefono))

            connection.commit()
            return "Client registered successfully!"  # Return success message
        except Exception as error:
            return f"Error registering client: {str(error)}"  # Return error message
        finally:
            cursor.close()
            connection.close()  # Always close the connection
    else:
        return "Failed to connect to the database."  # Return connection error message
