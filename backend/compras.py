import psycopg2  # Conexión a PostgreSQL (Servidor Central)
import pyodbc    # Conexión a SQL Server (Nodo Local)

# Conexión al Servidor Central (PostgreSQL)
def conectar_postgres():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="Proyecto2",
            user="admin",
            password="admin",
            options="-c client_encoding=UTF8"
        )
        return connection
    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None

# Conexión al Nodo Local (SQL Server)
def conectar_sqlserver():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LaptpMajo-1803;'
            'DATABASE=Proyecto2-NL;'
            'UID=admin;'
            'PWD=admin'
        )
        return connection
    except Exception as e:
        print(f"Error al conectar con SQL Server: {e}")
        return None

# Verificar promociones en el servidor central
def verificar_promocion(connection, id_nodo):
    query = "SELECT descuento FROM promociones WHERE id_nodo = %s;"
    connection.execute(query, (id_nodo,))
    promocion = connection.fetchone()
    if promocion:
        return promocion[0]  # Porcentaje de descuento
    return 0  # No hay descuento

# Verificar saldo del cliente en el monedero central
def verificar_saldo(connection, id_cliente):
    query = "SELECT saldo FROM monedero WHERE id_cliente = %s;"
    connection.execute(query, (id_cliente,))
    monedero = connection.fetchone()
    if monedero:
        return monedero[0]  # Saldo disponible
    return 0

# Función para reducir saldo en el monedero del servidor central
def descargar_monedero(connection, id_cliente, monto):
    saldo_actual = verificar_saldo(connection, id_cliente)
    
    if saldo_actual >= monto:
        query_update_saldo = "UPDATE monedero SET saldo = saldo - %s WHERE id_cliente = %s;"
        connection.execute(query_update_saldo, (monto, id_cliente))

        query_insert_transaccion = """
            INSERT INTO transacciones (id_monedero, monto)
            SELECT id_monedero, %s FROM monedero WHERE id_cliente = %s;
        """
        connection.execute(query_insert_transaccion, (-monto, id_cliente))  # Montos negativos son descargas
        return True  # Transacción exitosa
    else:
        return False  # Saldo insuficiente

# Función para añadir saldo al monedero del servidor central
def recargar_monedero(connection, id_cliente, monto):
    query_update_saldo = "UPDATE monedero SET saldo = saldo + %s WHERE id_cliente = %s;"
    connection.execute(query_update_saldo, (monto, id_cliente))

    query_insert_transaccion = """
        INSERT INTO transacciones (id_monedero, monto)
        SELECT id_monedero, %s FROM monedero WHERE id_cliente = %s;
    """
    connection.execute(query_insert_transaccion, (monto, id_cliente))  # Montos positivos son recargas

# Registrar la venta en el nodo local
def registrar_venta(connection, id_producto, cantidad, precio_total, id_cliente):
    query = """
        INSERT INTO ventas (id_producto, cantidad, precio_total, id_cliente)
        VALUES (?, ?, ?, ?);
    """
    connection.execute(query, (id_producto, cantidad, precio_total, id_cliente))

def procesar_compra(id_cliente, id_producto, cantidad, id_nodo):
    # Conectar a las bases de datos
    conn_central = conectar_postgres()
    conn_local = conectar_sqlserver()
    
    if conn_central is None or conn_local is None:
        print("No se pudo conectar a una de las bases de datos.")
        return

    try:
        cursor_central = conn_central.cursor()
        cursor_local = conn_local.cursor()

        # Verificar si hay promociones activas
        descuento = verificar_promocion(cursor_central, id_nodo)

        # Obtener el precio del producto desde el nodo local
        query_producto = "SELECT precio FROM productos WHERE id_producto = ?"
        cursor_local.execute(query_producto, (id_producto,))
        producto = cursor_local.fetchone()

        if producto:
            precio_producto = producto[0]
            precio_total = precio_producto * cantidad

            # Aplicar descuento si existe
            if descuento > 0:
                precio_total = precio_total * (1 - (descuento / 100))

            # Reducir saldo del cliente si es suficiente
            if descargar_monedero(cursor_central, id_cliente, precio_total):
                # Registrar la venta en el nodo local
                registrar_venta(cursor_local, id_producto, cantidad, precio_total, id_cliente)

                # Guardar los cambios en ambas bases de datos
                conn_local.commit()
                conn_central.commit()

                print("Compra realizada con éxito.")
            else:
                print("Saldo insuficiente.")
        else:
            print("Producto no encontrado.")

    except Exception as e:
        print(f"Error procesando la compra: {e}")
        conn_local.rollback()
        conn_central.rollback()
    finally:
        cursor_central.close()
        cursor_local.close()
        conn_central.close()
        conn_local.close()
