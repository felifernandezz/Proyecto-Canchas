from extensiones import db

class Establecimiento(db.Model):
    __tablename__ = 'establecimientos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    canchas = db.relationship('Cancha', backref='establecimiento', lazy=True)
    horarios = db.relationship('Horario', backref='establecimiento', lazy=True)

  