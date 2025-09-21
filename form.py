from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms import DateField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length

# -----------------------------
# Formulario para PRODUCTO
# -----------------------------
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    talla = StringField('Talla', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

# -----------------------------
# Formulario para CLIENTE
# -----------------------------
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    cedula = StringField('Cédula', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Guardar')

# -----------------------------
# Formulario para DETALLE_VENTAS1
# -----------------------------
class DetalleVentaForm(FlaskForm):
    id_producto = SelectField('Producto', coerce=int, validators=[DataRequired()])
    id_cliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio_unitario = FloatField('Precio Unitario', validators=[DataRequired(), NumberRange(min=0.01)])
    descuento = FloatField('Descuento', validators=[NumberRange(min=0)], default=0)
    despacho = StringField('Despacho')
    fidelidad = StringField('Fidelidad')
    submit = SubmitField('Guardar')

# -----------------------------
# Formulario para FACTURA
# -----------------------------
class FacturaForm(FlaskForm):
    fecha_factura = DateField('Fecha de la Factura', format='%Y-%m-%d', validators=[DataRequired()])
    id_cliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    id_empleado = SelectField('Empleado', coerce=int, validators=[DataRequired()])
    valor_total = DecimalField('Valor Total', places=2, validators=[DataRequired(), NumberRange(min=0)])
    iva = DecimalField('IVA', places=2, validators=[DataRequired(), NumberRange(min=0)])
    id_producto = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Guardar Factura')