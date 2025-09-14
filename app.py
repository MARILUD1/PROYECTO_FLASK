import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf import FlaskForm

# Importa las funciones de tu archivo de base de datos
from inventario import (
    crear_tablas, 
    insertar_producto, 
    obtener_todos, 
    buscar_por_nombre,
    eliminar_producto
)
from forms import ProductoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_segura'

@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/formulario_productos', methods=['GET', 'POST'])
def formulario_productos():
    form = ProductoForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        
        try:
            insertar_producto(nombre, cantidad, precio)
            flash(f'Producto "{nombre}" registrado correctamente!', 'success')
            return redirect(url_for('lista_productos'))
        except sqlite3.IntegrityError:
            flash(f'Error: El producto "{nombre}" ya existe.', 'danger')
    
    return render_template('productos/formulario_productos.html', form=form, title='Nuevo Producto')

@app.route('/lista_productos')
def lista_productos():
    q = request.args.get('q', '')
    
    if q:
        productos = buscar_por_nombre(q)
    else:
        productos = obtener_todos()

    return render_template('productos/lista_productos.html', productos=productos, title='Lista de Productos', q=q)

@app.route('/eliminar_producto/<int:pid>', methods=['POST'])
def eliminar_producto_route(pid):
    eliminar_producto(pid)
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for('lista_productos'))

if __name__ == "__main__":
    with app.app_context():
        crear_tablas()
    app.run(debug=True)