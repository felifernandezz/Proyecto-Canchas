from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensiones import db
from modelos.reserva import Reserva

reservar_cancha_bp = Blueprint('reservar_cancha_bp', __name__)

@reservar_cancha_bp.route('/', methods=['POST'])
@jwt_required()
def reservar_cancha():
    user_id = get_jwt_identity()
    data = request.get_json()
    nueva_reserva = Reserva(
        usuario_id=user_id,
        cancha_id=data['cancha_id'],
        fecha_hora=data['fecha_hora'],
        estado="reservada"
    )
    db.session.add(nueva_reserva)
    db.session.commit()
    return jsonify({"msg": "Reserva realizada exitosamente", "reserva_id": nueva_reserva.id}), 201
