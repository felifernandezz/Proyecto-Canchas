from extensiones import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="cliente")  # "dueño" o "cliente"

    establecimientos = db.relationship('Establecimiento', backref='duenio', lazy=True)
    reservas = db.relationship('Reserva', backref='cliente', lazy=True)
