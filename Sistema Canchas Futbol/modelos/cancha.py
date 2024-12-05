from extensiones import db

class Cancha(db.Model):
    __tablename__ = 'canchas'

    id = db.Column(db.Integer, primary_key=True)
    tipo_cancha = db.Column(db.String(10), nullable=False)  # Ejemplo: "5", "7", "8", "9", "11"
    cantidad = db.Column(db.Integer, nullable=False)
    establecimiento_id = db.Column(db.Integer, db.ForeignKey('establecimientos.id'), nullable=False)
    precio = db.Column(db.Float, nullable=False)  # Precio por hora o unidad de tiempo
    
    reservas = db.relationship('Reserva', backref='cancha', lazy=True)


    def toDict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo_cancha,
            'estado': self.estado
        }
