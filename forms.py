from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(message="El nombre es obligatorio."), Length(min=2, max=50)]
    )
    cantidad = IntegerField(
        'Cantidad',
        validators=[DataRequired(message="La cantidad es obligatoria."),
                    NumberRange(min=0, message="Debe ser un número positivo.")]
    )
    precio = FloatField(
        'Precio',
        validators=[DataRequired(message="El precio es obligatorio."),
                    NumberRange(min=0.01, message="Debe ser un número positivo.")]
    )
    submit = SubmitField('Guardar')