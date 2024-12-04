from extensiones import db

class Horarios(db.Model):
    __tablename__ = 'horarios'

    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    establecimiento_id = db.Column(db.Integer, db.ForeignKey('establecimientos.id'), nullable=False)
