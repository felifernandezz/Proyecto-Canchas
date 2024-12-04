from flask import Blueprint, jsonify, request
from extensiones import db
from modelos.reserva import Reserva
from datetime import datetime, timedelta

cancelar_reserva_bp = Blueprint('cancelar_reserva_bp', __name__)

@cancelar_reserva_bp.route('/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    limite_cancelacion = reserva.fecha_hora - timedelta(hours=6)

    if datetime.now() > limite_cancelacion:
        return jsonify({"msg": "No podes cancelar una reserva dentro de las próximas 6 horas."}), 400

    reserva.estado = 'cancelada'
    db.session.commit()
    return jsonify({"msg": "La reserva ha sido cancelada exitosamente."}), 200
