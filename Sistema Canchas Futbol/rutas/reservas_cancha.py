from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from extensiones import db
from modelos.reserva import Reserva
from modelos.horarios import Horarios
from datetime import datetime, timedelta

reservas_cancha_bp = Blueprint('reservas_cancha_bp', __name__)

@reservas_cancha_bp.route('/reservar', methods=['POST'])
def reservar_cancha():
    data = request.get_json()
    tipo_cancha = data.get('tipo_cancha')
    fecha_hora = data.get('fecha_hora')
    nombre = data.get('nombre')
    telefono = data.get('telefono')

    # Verificar disponibilidad de canchas en el horario solicitado
    cancha = cancha.query.filter_by(tipo_cancha=tipo_cancha).first()
    if not cancha:
        return jsonify({"msg": "No existe este tipo de cancha."}), 404

    # Contar cuántas reservas ya existen para ese tipo de cancha y horario
    reservas_existentes = Reserva.query.filter_by(cancha_id=cancha.id, fecha_hora=fecha_hora).count()

    # Verificar si hay disponibilidad
    if reservas_existentes >= cancha.cantidad:
        return jsonify({"msg": "No hay canchas disponibles para ese horario."}), 400

    # Crear la nueva reserva
    nueva_reserva = Reserva(
        nombre=nombre,
        telefono=telefono,
        cancha_id=cancha.id,
        fecha_hora=fecha_hora
    )
    db.session.add(nueva_reserva)
    db.session.commit()

    return jsonify({"msg": "Reserva realizada con éxito"}), 201


@reservas_cancha_bp.route('/horarios_disponibles', methods=['GET'])
def obtener_horarios_disponibles():
    # Obtener los parámetros de la fecha y cancha
    cancha_id = request.args.get('cancha_id', type=int)
    fecha_str = request.args.get('fecha', type=str)  # Formato de fecha: 'YYYY-MM-DD'
    
    if not cancha_id or not fecha_str:
        return jsonify({"msg": "Se requiere cancha_id y fecha."}), 400
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convierte la fecha de string a date
    except ValueError:
        return jsonify({"msg": "Fecha inválida."}), 400
    
    # Obtener los horarios disponibles para la fecha y la cancha
    horarios = Horarios.query.filter_by(establecimiento_id=cancha_id).all()
    
    # Generar una lista de horarios disponibles
    horarios_disponibles = []
    for horario in horarios:
        # Verificar si el horario está libre para esa fecha
        hora_inicio = datetime.combine(fecha, horario.hora_inicio)
        hora_fin = datetime.combine(fecha, horario.hora_fin)
        
        # Comprobar si ya hay reservas para este horario
        reserva_existente = Reserva.query.filter_by(cancha_id=cancha_id, fecha_hora=hora_inicio).first()
        if not reserva_existente:
            horarios_disponibles.append({
                "hora_inicio": hora_inicio.strftime("%H:%M"),
                "hora_fin": hora_fin.strftime("%H:%M")
            })
    
    return jsonify(horarios_disponibles)
