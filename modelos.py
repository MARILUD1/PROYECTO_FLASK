# app.py o modelos.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb

# ----------------------------
# Conexión a la base de datos
# ----------------------------
def conexion():
    return mariadb.connect(
        host="localhost",
        user="root",
        password="Lupe1986.",
        database="almacenropalamoda"
    )

def cerrar_conexion(conn):
    if conn:
        conn.close()

# ----------------------------
# Clase Usuario para Flask-Login
# ----------------------------
class Usuario(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = conexion()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE id_usuarios = ?", (id_usuario,))
        usuario_db = cur.fetchone()
        cerrar_conexion(conn)
        if usuario_db:
            return Usuario(
                id=usuario_db['id_usuarios'],
                nombre=usuario_db['nombre'],
                email=usuario_db['email'],
                password=usuario_db['password']
            )
        return None

    @staticmethod
    def obtener_por_email(email):
        conn = conexion()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario_db = cur.fetchone()
        cerrar_conexion(conn)
        if usuario_db:
            return Usuario(
                id=usuario_db['id_usuarios'],
                nombre=usuario_db['nombre'],
                email=usuario_db['email'],
                password=usuario_db['password']
            )
        return None

    def verificar_password(self, password):
        # check_password_hash compara el hash guardado con la contraseña ingresada
        return check_password_hash(self.password, password)

# ----------------------------
# Configuración para Flask-Login
# ----------------------------
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.obtener_por_id(id_usuario)