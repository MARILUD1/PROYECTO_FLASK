# clase de conexion a BD sin sqlalchemy 
import mariadb
import sys

# conexion a la base de datos

def conexion():
    return mariadb.connect(
        host='localhost',
        database='BasededatosFlask',
        user='Flask',  # luego en producción usa variable de entorno
        password='Lupe1986.' # luego en producción usa variable de entorno
    )

# cerrar conexion a la base de datos

def cerrar_conexion(conn):
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada.")
# probar conexion a la base de datos