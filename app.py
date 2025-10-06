# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import mariadb
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from form import ProductoForm, ClienteForm, DetalleVentaForm, FacturaForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# ----------------------------
# Inicialización de la aplicación
# ----------------------------
app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ----------------------------
# Conexión a la base de datos
# ----------------------------
def conexion():
    return mariadb.connect(
        host="localhost",
        user="root",
        password="Lupe1986.",
        database="BasededatosFlask"
    )

def cerrar_conexion(conn):
    if conn:
        conn.close()


# Clase Usuario para Flask-Login
# ----------------------------
class Usuario(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id)

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
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

# ----------------------------
# Rutas de autenticación
# ----------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = conexion()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            if cur.fetchone():
                flash("El correo electrónico ya está registrado.", "danger")
                return redirect(url_for('registro'))
            
            hashed_password = generate_password_hash(password)
            cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", 
                        (nombre, email, hashed_password))
            conn.commit()
            flash("¡Registro exitoso! Ya puedes iniciar sesión.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar el usuario: {e}", "danger")
        finally:
            cerrar_conexion(conn)

    return render_template('registro.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario_encontrado = Usuario.obtener_por_email(email)
        
        if usuario_encontrado and usuario_encontrado.verificar_password(password):
            login_user(usuario_encontrado)
            flash(f"¡Bienvenido, {usuario_encontrado.nombre}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Correo electrónico o contraseña incorrectos.", "danger")
            
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('login'))
    
# ----------------------------
# Rutas de Usuarios
# ----------------------------
@app.route("/usuarios")
@login_required
def lista_usuarios():
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_usuarios, nombre, email FROM usuarios")
        usuarios = cur.fetchall()
        return render_template("usuario_cliente.html", usuarios=usuarios, title="Lista de Usuarios")
    except Exception as e:
        flash(f"Error al cargar la lista de usuarios: {e}", "danger")
        usuarios = []
        return render_template("usuario_cliente.html", usuarios=usuarios, title="Lista de Usuarios")
    finally:
        cerrar_conexion(conn)

# ----------------------------
# Rutas de inicio
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

# ----------------------------
# Rutas de Productos
# Listar / Buscar Productos

@app.route('/producto')
@login_required
def lista_producto():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Número de productos por página
    offset = (page - 1) * per_page
    
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    
    # Obtener el número total de productos para la paginación
    if q:
        cur.execute("SELECT COUNT(*) AS total FROM producto WHERE nombre LIKE ?", (f"%{q}%",))
    else:
        cur.execute("SELECT COUNT(*) AS total FROM producto")
        
    total = cur.fetchone()['total']

    # Obtener los productos para la página actual
    if q:
        cur.execute("SELECT * FROM producto WHERE nombre LIKE ? LIMIT ? OFFSET ?", (f"%{q}%", per_page, offset))
    else:
        cur.execute("SELECT * FROM producto LIMIT ? OFFSET ?", (per_page, offset))
    
    productos = cur.fetchall()
    
    # Calcular el número total de páginas
    pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    cerrar_conexion(conn)

    return render_template(
        'producto/lista_producto.html',
        title='Productos',
        producto=productos,
        q=q,
        page=page,
        pages=pages,
        total=total
    )

# Crear Producto
@app.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO producto (nombre, cantidad, talla, color, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
                (form.nombre.data, form.cantidad.data, form.talla.data, form.color.data, form.precio.data, form.stock.data)
            )
            conn.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('lista_producto'))
        except Exception as e:
            conn.rollback()
            flash(f'No se pudo guardar: {str(e)}', 'danger')
        finally:
            cerrar_conexion(conn)
    return render_template('producto/formulario_producto.html', title='Nuevo producto', form=form)

# Editar Producto
@app.route('/producto/<int:pid>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(pid):
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE id_producto = ?", (pid,))
    prod = cur.fetchone()
    
    if not prod:
        cerrar_conexion(conn)
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("lista_producto"))

    form = ProductoForm(data=prod)
    if form.validate_on_submit():
        try:
            cur.execute(
                "UPDATE producto SET nombre=?, cantidad=?, talla=?, color=?, precio=?, stock=? WHERE id_producto=?",
                (form.nombre.data, form.cantidad.data, form.talla.data, form.color.data, form.precio.data, form.stock.data, pid)
            )
            conn.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('lista_producto'))
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    cerrar_conexion(conn)
    return render_template('producto/formulario_producto.html', title='Editar producto', form=form, pid=pid)

# Eliminar Producto
@app.route('/producto/<int:pid>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(pid):
    conn = conexion()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM producto WHERE id_producto = ?", (pid,))
        if cur.rowcount > 0:
            conn.commit()
            flash('Producto eliminado correctamente.', 'success')
        else:
            flash('Producto no encontrado.', 'warning')
    except Exception as e:
        conn.rollback()
        flash(f"Error al eliminar el producto: {e}", "danger")
    finally:
        cerrar_conexion(conn)
    return redirect(url_for('lista_producto'))

# Rutas de Clientes

@app.route("/clientes")
@login_required
def lista_clientes():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Número de clientes visibles por página
    offset = (page - 1) * per_page

    conn = conexion()
    cur = conn.cursor(dictionary=True) # Se usa dictionary=True para facilitar el acceso a los datos

    # 1. Obtener el número total de clientes
    if q:
        cur.execute(
            "SELECT COUNT(*) AS total FROM clientes WHERE nombre LIKE ? OR apellidos LIKE ? OR cedula LIKE ?",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        )
    else:
        cur.execute("SELECT COUNT(*) AS total FROM clientes")
    
    total = cur.fetchone()['total']

    # 2. Obtener los clientes para la página actual
    if q:
        cur.execute(
            "SELECT * FROM clientes WHERE nombre LIKE ? OR apellidos LIKE ? OR cedula LIKE ? LIMIT ? OFFSET ?",
            (f"%{q}%", f"%{q}%", f"%{q}%", per_page, offset)
        )
    else:
        cur.execute("SELECT * FROM clientes LIMIT ? OFFSET ?", (per_page, offset))
        
    clientes = cur.fetchall()
    
    # Calcular el número total de páginas
    pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    cerrar_conexion(conn)
    
    return render_template(
        "clientes/lista_clientes.html", 
        clientes=clientes, 
        q=q,
        page=page,
        pages=pages
    )

@app.route("/clientes/crear", methods=["GET", "POST"])
@login_required
def crear_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = conexion()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO clientes (nombre, apellidos, cedula, correo, telefono) VALUES (?, ?, ?, ?, ?)",
                (form.nombre.data, form.apellidos.data, form.cedula.data, form.correo.data, form.telefono.data)
            )
            conn.commit()
            flash("Cliente creado correctamente", "success")
            return redirect(url_for("lista_clientes"))
        except Exception as e:
            conn.rollback()
            flash(f"Error al crear el cliente: {e}", "danger")
        finally:
            cerrar_conexion(conn)
            
    return render_template("clientes/formulario_cliente.html", form=form, title="Crear Cliente")

@app.route("/clientes/editar/<int:cid>", methods=["GET", "POST"])
@login_required
def editar_cliente(cid):
    conn = conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes WHERE id_cliente = ?", (cid,))
    cliente = cur.fetchone()
    
    if not cliente:
        cerrar_conexion(conn)
        flash("Cliente no encontrado", "danger")
        return redirect(url_for("lista_clientes"))
        
    form = ClienteForm(data={
        'nombre': cliente[1], 'apellidos': cliente[2], 'cedula': cliente[3],
        'correo': cliente[4], 'telefono': cliente[5]
    })
    
    if form.validate_on_submit():
        try:
            cur.execute(
                "UPDATE clientes SET nombre=?, apellidos=?, cedula=?, correo=?, telefono=? WHERE id_cliente=?",
                (form.nombre.data, form.apellidos.data, form.cedula.data, form.correo.data, form.telefono.data, cid)
            )
            conn.commit()
            flash("Cliente actualizado correctamente", "success")
            return redirect(url_for("lista_clientes"))
        except Exception as e:
            conn.rollback()
            flash(f"Error al actualizar el cliente: {e}", "danger")
        finally:
            cerrar_conexion(conn)
    
    return render_template("clientes/formulario_cliente.html", form=form, title="Editar Cliente", cid=cid)

@app.route("/clientes/eliminar/<int:cid>", methods=["POST"])
@login_required
def eliminar_cliente(cid):
    conn = conexion()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM clientes WHERE id_cliente=?", (cid,))
        conn.commit()
        if cur.rowcount > 0:
            flash("Cliente eliminado correctamente", "success")
        else:
            flash("Cliente no encontrado.", "warning")
    except Exception as e:
        conn.rollback()
        flash(f"Error al eliminar el cliente: {e}", "danger")
    finally:
        cerrar_conexion(conn)
    return redirect(url_for("lista_clientes"))

# Rutas de Detalle de Ventas

@app.route("/detalle_ventas")
@login_required
def lista_detalle_ventas():
    # Parámetros de paginación y búsqueda
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    # Usamos 3 como en tu ejemplo de lista_producto
    per_page = 3  
    offset = (page - 1) * per_page
    
    conn = None
    detalles = []
    total = 0
    pages = 1
    
    try:
        conn = conexion()
        # Nota: Usaremos cursor(dictionary=True) para obtener resultados con nombres de columna
        cur = conn.cursor(dictionary=True) 
        
        # 1. Configurar la cláusula WHERE y parámetros para búsqueda
        where_clause = ""
        params = []
        if q:
            # Filtra por nombre/apellido del cliente o nombre del producto (asumiendo la misma lógica)
            where_clause = """
                WHERE c.nombre LIKE ? OR c.apellidos LIKE ? OR p.nombre LIKE ?
            """
            search_term = f"%{q}%"
            params = [search_term, search_term, search_term]
        
        # 2. Obtener el TOTAL de registros (para la paginación)
        cur.execute(f"""
            SELECT COUNT(dv.id_detalle) AS total FROM detalle_ventas1 dv
            JOIN clientes c ON dv.id_cliente = c.id_cliente
            JOIN producto p ON dv.id_producto = p.id_producto
            {where_clause}
        """, params)
        total = cur.fetchone()['total']
        
        # 3. Obtener los detalles de venta PAGINADOS
        # Los parámetros de paginación (LIMIT/OFFSET) se añaden al final de la lista de parámetros
        params_paged = params + [per_page, offset]
        
        cur.execute(f"""
            SELECT dv.id_detalle, c.nombre AS nombre_cliente, c.apellidos AS apellido_cliente, 
                   p.nombre AS nombre_producto, dv.cantidad, dv.descuento, dv.precio_unitario
            FROM detalle_ventas1 dv
            JOIN clientes c ON dv.id_cliente = c.id_cliente
            JOIN producto p ON dv.id_producto = p.id_producto
            {where_clause}
            ORDER BY dv.id_detalle DESC
            LIMIT ? OFFSET ?
        """, params_paged)
        detalles = cur.fetchall()
        
        # 4. Calcular el número total de páginas
        pages = (total // per_page) + (1 if total % per_page > 0 else 0)
        
    except Exception as e:
        flash(f"Error al cargar la lista de detalles de venta: {e}", "danger")
        
    finally:
        if conn:
            cerrar_conexion(conn)
    
    return render_template(
        "detalle_ventas1/lista_detalle_ventas.html", 
        title="Detalle de Ventas",
        detalles=detalles,
        q=q,
        page=page,
        pages=pages,
        total=total
    )

#================================================
# CREAR DETALLE DE VENTA
#================================================

@app.route("/detalle_ventas/crear", methods=["GET", "POST"])
@login_required
def crear_detalle_venta():
    form = DetalleVentaForm()
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        
        # Llenar opciones para los SelectFields
        cur.execute("SELECT id_cliente, nombre, apellidos FROM clientes")
        clientes = cur.fetchall()
        form.id_cliente.choices = [(c[0], f"{c[1]} {c[2]}") for c in clientes]
        
        cur.execute("SELECT id_producto, nombre FROM producto")
        productos = cur.fetchall()
        form.id_producto.choices = [(p[0], p[1]) for p in productos]
        
        cur.execute("SELECT id_factura, fecha_factura FROM factura ORDER BY id_factura DESC")
        facturas = cur.fetchall()
        # Nota: Se añade manejo de error si fecha_factura es NULL o no tiene strftime
        form.id_factura.choices = [(f[0], f"Factura #{f[0]} ({f[1].strftime('%Y-%m-%d') if f[1] else 'Sin fecha'})") for f in facturas]
        
        
        if form.validate_on_submit():
            cur.execute("""
                INSERT INTO detalle_ventas1 (id_factura, id_cliente, id_producto, cantidad, descuento, precio_unitario)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                form.id_factura.data,
                form.id_cliente.data,
                form.id_producto.data,
                form.cantidad.data, 
                form.descuento.data,
                form.precio_unitario.data
            ))
            
            conn.commit() 
            flash("Detalle de venta creado correctamente", "success")
            return redirect(url_for("lista_detalle_ventas"))

    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Error al crear el detalle de venta: {e}", "danger")
        
    finally:
        if conn:
            cerrar_conexion(conn)

    return render_template("detalle_ventas1/form_detalle_venta.html", form=form, title="Crear Detalle de Venta")

#================================================
# EDITAR DETALLE DE VENTA
#================================================

@app.route('/detalle_ventas/<int:did>/editar', methods=['GET', 'POST'])
@login_required
def editar_detalle_venta(did):
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor(dictionary=True)
        
        # 1. Cargar detalle existente
        cur.execute("SELECT * FROM detalle_ventas1 WHERE id_detalle = ?", (did,))
        detalle = cur.fetchone()
        
        if not detalle:
            flash("Detalle de venta no encontrado.", "danger")
            return redirect(url_for("lista_detalle_ventas"))

        # 2. Inicializar formulario con datos actuales y cargar opciones
        form = DetalleVentaForm(data=detalle)
        
        # Llenar opciones de SelectFields (igual que en 'crear')
        cur.execute("SELECT id_cliente, nombre, apellidos FROM clientes")
        form.id_cliente.choices = [(c[0], f"{c[1]} {c[2]}") for c in cur.fetchall()]
        
        cur.execute("SELECT id_producto, nombre FROM producto")
        form.id_producto.choices = [(p[0], p[1]) for p in cur.fetchall()]
        
        cur.execute("SELECT id_factura, fecha_factura FROM factura ORDER BY id_factura DESC")
        facturas = cur.fetchall()
        form.id_factura.choices = [(f[0], f"Factura #{f[0]} ({f[1].strftime('%Y-%m-%d') if f[1] else 'Sin fecha'})") for f in facturas]


        if form.validate_on_submit():
            # 3. Actualizar datos
            cur.execute(
                """
                UPDATE detalle_ventas1 SET id_factura=?, id_cliente=?, id_producto=?, cantidad=?, 
                                          despacho=?, fidelidad=?, descuento=?, precio_unitario=? 
                WHERE id_detalle=?
                """,
                (form.id_factura.data, form.id_cliente.data, form.id_producto.data, form.cantidad.data, 
                 form.despacho.data, form.fidelidad.data, form.descuento.data, form.precio_unitario.data, did)
            )
            conn.commit()
            flash('Detalle de venta actualizado correctamente.', 'success')
            return redirect(url_for('lista_detalle_ventas'))
        
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error al actualizar el detalle: {str(e)}', 'danger')
        
    finally:
        if conn:
            cerrar_conexion(conn)

    return render_template('detalle_ventas1/form_detalle_venta.html', title='Editar Detalle de Venta', form=form, did=did)

#================================================
# ELIMINAR DETALLE DE VENTA
#================================================

@app.route('/detalle_ventas/<int:did>/eliminar', methods=['POST'])
@login_required
def eliminar_detalle_venta(did):
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM detalle_ventas1 WHERE id_detalle = ?", (did,))
        
        if cur.rowcount > 0:
            conn.commit()
            flash('Detalle de venta eliminado correctamente.', 'success')
        else:
            flash('Detalle de venta no encontrado.', 'warning')
            
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Error al eliminar el detalle de venta: {e}", "danger")
        
    finally:
        if conn:
            cerrar_conexion(conn)
            
    return redirect(url_for('lista_detalle_ventas'))








# ----------------------------
# Rutas de Facturas
# ----------------------------
# app.py


@app.route("/facturas")
@login_required
def lista_facturas():
    conn = conexion()
    cur = conn.cursor(dictionary=True) 
    try:
        cur.execute("""
            SELECT
                f.id_factura,
                f.fecha_factura,
                c.nombre as nombre_cliente,
                -- Se elimina la referencia a 'e.nombre'
                f.valor_total,
                f.iva
            FROM factura f
            JOIN clientes c ON f.id_cliente = c.id_cliente
            -- Se elimina la línea JOIN empleado
            ORDER BY f.id_factura DESC
        """)
        facturas = cur.fetchall()
    except Exception as e:
        flash(f"Error al cargar las facturas: {e}", "danger")
        facturas = []
    finally:
        cerrar_conexion(conn)
    
    return render_template("factura/lista_facturas.html", facturas=facturas, title="Lista de Facturas")

# ... (código para crear_factura)
@app.route("/facturas/crear", methods=["GET", "POST"])
@login_required
def crear_factura():
    form = FacturaForm()
    conn = conexion()
    cur = conn.cursor()
    
    cur.execute("SELECT id_cliente, nombre, apellidos FROM clientes")
    clientes = cur.fetchall()
    form.id_cliente.choices = [(c[0], f"{c[1]} {c[2]}") for c in clientes]
    
    
    cur.execute("SELECT id_producto, nombre FROM producto")
    productos = cur.fetchall()
    form.id_producto.choices = [(p[0], p[1]) for p in productos]
    
    if form.validate_on_submit():
        try:
            cur.execute("""
                INSERT INTO factura (fecha_factura, id_cliente, valor_total, iva)
                VALUES (?, ?, ?, ?)
            """, (
                form.fecha_factura.data,
                form.id_cliente.data,
                form.valor_total.data,
                form.iva.data,
            ))
            conn.commit()
            flash("Factura creada correctamente", "success")
            return redirect(url_for("lista_facturas"))
        except mariadb.Error as e:
            conn.rollback()
            flash(f"Error al crear la factura: {e}", "danger")
        finally:
            cerrar_conexion(conn)
            
    return render_template("factura/formulario_factura.html", form=form, title="Crear Factura")

if __name__ == "__main__":
    app.run(debug=True)