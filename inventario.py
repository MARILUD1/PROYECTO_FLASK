import sqlite3

DB_NAME = "inventario.db"

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        """)
        conn.commit()

def insertar_producto(nombre, cantidad, precio):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (nombre, cantidad, precio))
        conn.commit()

def eliminar_producto(id_producto):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        conn.commit()

def obtener_todos():
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        return [Producto(row['id_producto'], row['nombre'], row['cantidad'], row['precio']) for row in rows]

def buscar_por_nombre(nombre):
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        rows = cursor.fetchall()
        return [Producto(row['id_producto'], row['nombre'], row['cantidad'], row['precio']) for row in rows]