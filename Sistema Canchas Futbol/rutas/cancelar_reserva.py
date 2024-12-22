from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from extensiones import obtener_conexion

cancelar_reserva_bp = Blueprint('cancelar_reserva_bp', __name__)

@cancelar_reserva_bp.route('/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    """
    Permite cancelar una reserva si aún no está dentro de las próximas 6 horas.
    """
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Obtener información de la reserva
        query_reserva = "SELECT fecha_hora, estado FROM reservas WHERE id = %s"
        cursor.execute(query_reserva, (reserva_id,))
        reserva = cursor.fetchone()

        # Si no se encuentra la reserva
        if not reserva:
            cursor.close()
            conexion.close()
            return jsonify({"msg": "Reserva no encontrada"}), 404

        # Calcular el límite de cancelación
        fecha_hora_reserva = reserva['fecha_hora']
        limite_cancelacion = fecha_hora_reserva - timedelta(hours=6)

        if datetime.now() > limite_cancelacion:
            cursor.close()
            conexion.close()
            return jsonify({"msg": "No podes cancelar una reserva dentro de las próximas 6 horas."}), 400

        # Actualizar el estado de la reserva a 'cancelada'
        query_update = "UPDATE reservas SET estado = %s WHERE id = %s"
        cursor.execute(query_update, ('cancelada', reserva_id))
        conexion.commit()

        # Cerrar conexiones
        cursor.close()
        conexion.close()

        return jsonify({"msg": "La reserva ha sido cancelada exitosamente."}), 200

    except Exception as e:
        print(f"Error al cancelar la reserva: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500

@cancelar_reserva_bp.route('/reservas', methods=['GET'])
def ver_reservas():
    """
    Permite obtener todas las reservas registradas.
    """
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Consultar todas las reservas
        query_reservas = """
        SELECT r.id, r.fecha_hora, r.estado, u.nombre AS cliente, u.telefono, c.tipo_cancha
        FROM reservas r
        JOIN usuarios u ON r.user_id = u.id
        JOIN canchas c ON r.cancha_id = c.id
        """
        cursor.execute(query_reservas)
        reservas = cursor.fetchall()

        # Cerrar conexiones
        cursor.close()
        conexion.close()

        return jsonify(reservas), 200

    except Exception as e:
        print(f"Error al obtener reservas: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500
