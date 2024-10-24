#crear la coneccion a las bases de datos
#primera base : central - Postgres

import psycopg2
import pyodbc
 
# Connection to PostgreSQL
def connect_postgresql():
    try:
        connection = psycopg2.connect(
            host="localhost",  
            database="Proyecto2",
            user="admin",
            password="admin",
            options="-c client_encoding=UTF8"
        )
        print("PostgreSQL connection successful")
        return connection
    except Exception as error:
        print(f"Error connecting to PostgreSQL: {error}")
        return None
    
#segunda base : nodos locales- SQLServer
# Connection to SQLServer
def connect_sqlserver():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=Proyecto2-NL;'
            'UID=admin;'
            'PWD=admin'
        )

        print("SQLServer connection successful")
        return connection
    except Exception as error:
        print(f"Error connecting to SQLServer: {error}")
        return None
    

