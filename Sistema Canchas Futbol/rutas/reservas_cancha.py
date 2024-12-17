from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from extensiones import obtener_conexion
from datetime import datetime, timedelta

reservas_cancha_bp = Blueprint('reservas_cancha_bp', __name__)

@reservas_cancha_bp.route('/reservar', methods=['POST'])
def reservar_cancha():
    data = request.get_json()
    tipo_cancha = data.get('tipo_cancha')
    fecha_hora = data.get('fecha_hora')
    nombre = data.get('nombre')
    telefono = data.get('telefono')

    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Verificar si existe la cancha
        query = "SELECT * FROM canchas WHERE tipo_cancha = %s"
        cursor.execute(query, (tipo_cancha,))
        cancha = cursor.fetchone()

        if not cancha:
            cursor.close()
            conexion.close()
            return jsonify({"msg": "No existe este tipo de cancha."}), 404

        # Contar cuántas reservas ya existen para ese tipo de cancha y horario
        query_reservas = "SELECT COUNT(*) FROM reservas WHERE cancha_id = %s AND fecha_hora = %s"
        cursor.execute(query_reservas, (cancha['id'], fecha_hora))
        reservas_existentes = cursor.fetchone()['COUNT(*)']

        # Verificar si hay disponibilidad
        if reservas_existentes >= cancha['cantidad']:
            cursor.close()
            conexion.close()
            return jsonify({"msg": "No hay canchas disponibles para ese horario."}), 400

        # Crear la nueva reserva
        query_insert = """
        INSERT INTO reservas (nombre, telefono, cancha_id, fecha_hora)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert, (nombre, telefono, cancha['id'], fecha_hora))
        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({"msg": "Reserva realizada con éxito"}), 201

    except Exception as e:
        print(f"Error al realizar la reserva: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500


@reservas_cancha_bp.route('/horarios_disponibles', methods=['GET'])
def obtener_horarios_disponibles():
    cancha_id = request.args.get('cancha_id', type=int)
    fecha_str = request.args.get('fecha', type=str)  # Formato de fecha: 'YYYY-MM-DD'

    if not cancha_id or not fecha_str:
        return jsonify({"msg": "Se requiere cancha_id y fecha."}), 400

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convierte la fecha de string a date
    except ValueError:
        return jsonify({"msg": "Fecha inválida."}), 400

    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Obtener los horarios disponibles para la fecha y la cancha
        query_horarios = "SELECT * FROM horarios WHERE establecimiento_id = %s"
        cursor.execute(query_horarios, (cancha_id,))
        horarios = cursor.fetchall()

        horarios_disponibles = []
        for horario in horarios:
            hora_inicio = datetime.combine(fecha, horario['hora_inicio'])
            hora_fin = datetime.combine(fecha, horario['hora_fin'])

            # Comprobar si ya hay reservas para este horario
            query_reserva = "SELECT * FROM reservas WHERE cancha_id = %s AND fecha_hora = %s"
            cursor.execute(query_reserva, (cancha_id, hora_inicio))
            reserva_existente = cursor.fetchone()

            if not reserva_existente:
                horarios_disponibles.append({
                    "hora_inicio": hora_inicio.strftime("%H:%M"),
                    "hora_fin": hora_fin.strftime("%H:%M")
                })

        cursor.close()
        conexion.close()

        return jsonify(horarios_disponibles)

    except Exception as e:
        print(f"Error al obtener horarios disponibles: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500
