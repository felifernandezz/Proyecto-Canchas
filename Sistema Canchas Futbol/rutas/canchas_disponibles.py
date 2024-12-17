from flask import Blueprint, jsonify
from extensiones import obtener_conexion

canchas_disponibles_bp = Blueprint('canchas_disponibles_bp', __name__)

@canchas_disponibles_bp.route('/tipos', methods=['GET'])
def obtener_tipos_canchas():
    """
    Devuelve todos los tipos de cancha y su cantidad disponible.
    """
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Consultar todos los tipos de cancha
        query = "SELECT tipo_cancha, cantidad FROM canchas"
        cursor.execute(query)
        canchas = cursor.fetchall()

        # Cerrar conexión
        cursor.close()
        conexion.close()

        # Retornar los datos de los tipos de cancha
        tipos_canchas = [{"tipo_cancha": cancha['tipo_cancha'], "cantidad": cancha['cantidad']} for cancha in canchas]
        return jsonify(tipos_canchas), 200

    except Exception as e:
        print(f"Error al obtener tipos de canchas: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500


@canchas_disponibles_bp.route('/cantidad/<int:cancha_id>', methods=['GET'])
def obtener_cantidad_de_un_tipoCancha(cancha_id):
    """
    Devuelve la cantidad disponible para un tipo específico de cancha.
    """
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Consultar la cancha por su ID
        query = "SELECT tipo_cancha, cantidad FROM canchas WHERE id = %s"
        cursor.execute(query, (cancha_id,))
        cancha = cursor.fetchone()

        if not cancha:
            cursor.close()
            conexion.close()
            return jsonify({"error": "No se encontró una cancha con ese ID"}), 404

        # Cerrar conexión
        cursor.close()
        conexion.close()

        # Retornar la cantidad de la cancha
        return jsonify({
            "tipo_cancha": cancha['tipo_cancha'],
            "cantidad_disponible": cancha['cantidad']
        }), 200

    except Exception as e:
        print(f"Error al obtener cantidad de cancha: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500
