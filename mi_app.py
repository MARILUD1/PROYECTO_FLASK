from flask import Flask

app = Flask(__name__)

# 1. Ruta 
@app.route('/')
def index():
    return '¡Hola, Bienvenidos!'

# 2. Nueva 
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Mi primera tarea Flask, {nombre}!'