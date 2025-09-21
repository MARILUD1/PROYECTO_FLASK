import sqlite3

DB_NAME = "inventario.db"

class Producto:
    def __init__(self, id_producto, nombre, cantidad, talla, color, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.talla = talla
        self.color = color
        self.precio = precio
        self.stock = stock

def conectar():
    """Conexión a la base de datos con filas como diccionarios"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                cantidad INTEGER NOT NULL,
                talla TEXT NOT NULL,
                color TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        conn.commit()

def insertar_producto(nombre, cantidad, talla, color, precio, stock):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, talla, color, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, cantidad, talla, color, precio, stock)
        )
        conn.commit()

def obtener_producto_por_id(id_producto):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto=?", (id_producto,))
        row = cursor.fetchone()
        if row:
            return Producto(
                row['id_producto'],
                row['nombre'],
                row['cantidad'],
                row['talla'],
                row['color'],
                row['precio'],
                row['stock']
            )
        return None

def editar_producto(id_producto, nombre, cantidad, talla, color, precio, stock):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, cantidad = ?, talla = ?, color = ?, precio = ?, stock = ?
            WHERE id_producto = ?
        """, (nombre, cantidad, talla, color, precio, stock, id_producto))
        conn.commit()

def eliminar_producto(id_producto):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        conn.commit()

def obtener_todos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        return [
            Producto(
                row['id_producto'],
                row['nombre'],
                row['cantidad'],
                row['talla'],
                row['color'],
                row['precio'],
                row['stock']
            )
            for row in rows
        ]

def buscar_por_nombre(nombre):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        rows = cursor.fetchall()
        return [
            Producto(
                row['id_producto'],
                row['nombre'],
                row['cantidad'],
                row['talla'],
                row['color'],
                row['precio'],
                row['stock']
            )
            for row in rows
        ]
