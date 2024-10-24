from connection import connect_postgresql  # Import the connection function
import qrcode
import io

def generate_qr_code(data):
    """Generate a QR code for the given data and return it as bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Use BytesIO to save the QR code image to a bytes buffer
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    
    # Get the byte data
    img_byte_array.seek(0)
    return img_byte_array.read()

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
            # Insert new client into the clientes table, including QR code as BYTEA
            qr_data = f"{cedula}-{correo}"
            qr_code_bytes = generate_qr_code(qr_data)

            cursor.execute("""
                INSERT INTO clientes (nombre, cedula, correo, telefono, qr_code)
                VALUES (%s, %s, %s, %s, %s) RETURNING id_cliente;
            """, (nombre, cedula, correo, telefono, qr_code_bytes))

            # Get the ID of the newly created client
            new_client_id = cursor.fetchone()[0]

            # Insert a new record into the monedero table with an initial saldo of 10,000
            cursor.execute("""
                INSERT INTO monedero (id_cliente, saldo)
                VALUES (%s, %s);
            """, (new_client_id, 0.0))

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
