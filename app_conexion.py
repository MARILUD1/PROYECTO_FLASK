# hacer con mysql.conector sin orm
from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import conexion, cerrar_conexion
from datetime import datetime
from forms import ProductoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta' # en producción usa una variable de entorno

# Inyectar "now" para usar {{ now().year }} en templates si quieres
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()} # ahora en los templates puedes usar {{ now().year }} para el año actual

# paginas Base
# productos
# listar y buscar
@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    if q:
        cursor.execute("SELECT * FROM productos WHERE LOWER(nombre) LIKE %s ORDER BY nombre", (f'%{q.lower()}%',))
    else:
        cursor.execute("SELECT * FROM productos ORDER BY nombre")

    productos = cursor.fetchall()
    cerrar_conexion(conn)
    # URL para la lista de productos
    return render_template('productos/lista_productos.html', productos=productos, title='Lista de Productos', q=q)

@app.route('/productos/nuevo', methods=['GET','POST'])
def crear_productos():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        cantidad = form.cantidad.data
        precio = form.precio.data
        conn = conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                           (nombre, cantidad, precio))
            conn.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except mysql.connector.IntegrityError:
            form.nombre.errors.append('Ya existe un producto con ese nombre.')
        finally:
            cerrar_conexion(conn)

    # URL para el formulario de nuevo producto
    return render_template('productos/formulario_productos.html', form=form, title='Nuevo Producto', modo='crear')

@app.route('/productos/<int:id>/eliminar', methods=['POST'])
def eliminar_producto(id):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    ok = cursor.rowcount > 0
    flash('Producto eliminado.' if ok else 'Producto no encontrado.', 'info' if ok else 'warning')
    return redirect(url_for('listar_productos'))

# about
@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

if __name__ == '__main__':
    app.run(debug=True)