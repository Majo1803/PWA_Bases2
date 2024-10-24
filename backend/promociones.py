from connection import connect_postgresql
def mostrar_promociones():
    conn_central = connect_postgresql()
    
    if conn_central is None:
        print("No se pudo conectar a la base de datos del servidor central.")
        return []

    promociones = []  # Inicializa una lista para almacenar promociones

    try:
        cursor_central = conn_central.cursor()

        # Consulta para obtener todas las promociones
        query = """
            SELECT p.id_promocion, p.descripcion, p.descuento, n.nombre AS nodo
            FROM promociones p
            LEFT JOIN nodos n ON p.id_nodo = n.id_nodo;
        """
        cursor_central.execute(query)

        # Obtener todos los registros
        promociones = cursor_central.fetchall()

        if promociones:
            print("Promociones disponibles:")
            for promo in promociones:
                id_promocion, descripcion, descuento, nodo = promo
                print(f"ID Promoción: {id_promocion}, Descripción: {descripcion}, Descuento: {descuento}%, Nodo: {nodo}")
        else:
            print("No hay promociones disponibles.")

    except Exception as e:
        print(f"Error al consultar promociones: {e}")
    finally:
        cursor_central.close()
        conn_central.close()
    
    return promociones  # Devuelve la lista de promociones
