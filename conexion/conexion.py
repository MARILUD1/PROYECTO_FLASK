
import mysql.connector

def conexion():
    return mysql.connector.connect(
    host= 'localhost',
        user= 'root',
        password='',
        dabase= 'almacenropalamoda'

    )
def cerrar_conexion(conn):
    if conn.is_connected():
        conn.close()
        print('conexion cerrada.')