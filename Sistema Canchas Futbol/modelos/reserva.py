from extensiones import db

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cancha_id = db.Column(db.Integer, db.ForeignKey('canchas.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)  # Combinando fecha y hora
    estado = db.Column(db.String(20), nullable=False, default="reservada")  # Ej: "reservada", "cancelada"
