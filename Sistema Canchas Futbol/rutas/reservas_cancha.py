from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from extensiones import db
from modelos.reserva import Reserva

reservas_cancha_bp = Blueprint('reservas_cancha_bp', __name__)

@reservas_cancha_bp.route('/reservar', methods=['POST'])
def realizar_reserva():
    data = request.get_json()
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    cancha_id = data.get('cancha_id')
    fecha_hora = data.get('fecha_hora')

    # Verificar disponibilidad de la cancha
    reserva_existente = Reserva.query.filter_by(cancha_id=cancha_id, fecha_hora=fecha_hora).first()
    if reserva_existente:
        return jsonify({"msg": "La cancha ya está reservada para esa fecha y hora."}), 400

    # Crear la reserva
    nueva_reserva = Reserva(nombre=nombre, telefono=telefono, cancha_id=cancha_id, fecha_hora=fecha_hora)
    db.session.add(nueva_reserva)
    db.session.commit()

    # Crear un token JWT
    token = create_access_token(identity={'nombre': nombre, 'telefono': telefono})

    return jsonify({"msg": "Reserva realizada con éxito", "token": token}), 201
