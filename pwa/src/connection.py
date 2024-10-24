# connection.py

import psycopg2

# Connection to PostgreSQL
def connect_postgresql():
    try:
        connection = psycopg2.connect(
            host="localhost",  
            database="Proyecto2",
            user="postgres",
            password="LaZonaMixta",
            options="-c client_encoding=UTF8"
        )
        print("PostgreSQL connection successful")
        return connection
    except Exception as error:
        print(f"Error connecting to PostgreSQL: {error}")
        return None
