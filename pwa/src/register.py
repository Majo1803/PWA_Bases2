import qrcode
import os
from connection import connect_postgresql  # Import the connection function

# Ruta donde se guardarán los QR generados
QR_FOLDER = 'static/qr_codes'

def generate_qr_code(cedula):
    """Genera un código QR basado en la cédula del cliente"""
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)  # Crea la carpeta si no existe

    # Crear el QR a partir de la cédula
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(cedula)
    qr.make(fit=True)

    # Generar imagen QR
    img = qr.make_image(fill='black', back_color='white')
    
    # Guardar imagen con el nombre del usuario basado en la cédula
    qr_filename = f"{cedula}.png"
    qr_filepath = os.path.join(QR_FOLDER, qr_filename)
    img.save(qr_filepath)
    
    return qr_filename  # Devuelve el nombre del archivo QR

def register_client(form_data):
    # Extracting data from the form
    nombre = form_data['nombre']
    cedula = form_data['cedula']
    correo = form_data['correo']
    telefono = form_data.get('telefono', '')  # Default to empty string if not provided

    # Generar código QR basado en la cédula
    qr_filename = generate_qr_code(cedula)

    # Connect to PostgreSQL and insert the new client
    connection = connect_postgresql()  # Use the connection function
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, cedula, correo, telefono, qr_code)
                VALUES (%s, %s, %s, %s, %s);
            """, (nombre, cedula, correo, telefono, qr_filename))

            connection.commit()
            return "Client registered successfully!"  # Return success message
        except Exception as error:
            return f"Error registering client: {str(error)}"  # Return error message
        finally:
            cursor.close()
            connection.close()  # Always close the connection
    else:
        return "Failed to connect to the database."  # Return connection error message
