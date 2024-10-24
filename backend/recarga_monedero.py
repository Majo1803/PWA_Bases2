# recargar_monedero.py
from connection import connect_postgresql

def recarga_monedero(id_usuario, id_monedero, monto):
    connection = None  # Inicializar la conexión aquí

    try:
        connection = connect_postgresql()
        cursor = connection.cursor()

        # Actualizar el saldo del monedero
        query = """
        UPDATE monedero SET saldo = saldo + %s WHERE id_monedero = %s
        """
        cursor.execute(query, (monto, id_monedero))
        connection.commit()

        # Registrar la transacción
        query_transaccion = """
        INSERT INTO transacciones (id_monedero, monto)
        VALUES (%s, %s)
        """
        cursor.execute(query_transaccion, (id_monedero, monto))
        connection.commit()

        print("Monto recargado al monedero exitosamente.")
    except Exception as error:
        print(f"Error al recargar el monedero: {error}")
    finally:
        if cursor:
            cursor.close()  # Cerrar el cursor
        if connection:
            connection.close()  # Cerrar la conexión

def descarga_monedero(connection, id_cliente, monto):
    try:
        cursor = connection.cursor()
        query = """
        UPDATE monedero SET saldo = saldo - %s WHERE id_cliente = %s AND saldo >= %s
        """
        cursor.execute(query, (monto, id_cliente, monto))
        connection.commit()

        query_transaccion = """
        INSERT INTO transacciones(id_monedero, monto)
        VALUES ((SELECT id_monedero FROM monedero WHERE id_cliente = %s), %s)
        """
        cursor.execute(query_transaccion, (id_cliente, -monto))
        connection.commit()

        print("Monto descontado del monedero exitosamente.")
    except Exception as error:
        print(f"Error al descontar del monedero: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()