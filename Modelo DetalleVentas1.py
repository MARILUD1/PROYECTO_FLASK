from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas1'  # nombre de la tabla
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    despacho = db.Column(db.String(100), nullable=False)
    fidelidad = db.Column(db.String(50), nullable=False)
    descuento = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    cliente = db.relationship("Cliente", backref="detalle_ventas")
    producto = db.relationship("Producto", backref="detalle_ventas")

    def __repr__(self):
        return f"<DetalleVenta Cliente:{self.id_cliente} Producto:{self.id_producto}>"
