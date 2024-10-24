
# src/get_client_info.py

from connection import connect_postgresql  # Import the connection function

def get_client_info(cliente_id):
    connection = connect_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre, cedula, correo, telefono FROM clientes WHERE id_cliente = %s;", (cliente_id,))
            client_info = cursor.fetchone()
            return client_info  # Return the client info as a tuple
        except Exception as error:
            print(f"Error retrieving client info: {error}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None
