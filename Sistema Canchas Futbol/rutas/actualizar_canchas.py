from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensiones import obtener_conexion

actualizar_canchas_bp = Blueprint('actualizar_canchas_bp', __name__)

def es_admin(user_id):
    """
    Verifica si el usuario tiene el rol de administrador en la base de datos.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT rol FROM usuarios WHERE id = %s"
        cursor.execute(query, (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        if usuario and usuario['rol'] == 'admin':
            return True
        return False
    except Exception as e:
        print(f"Error al verificar rol de administrador: {e}")
        return False

@actualizar_canchas_bp.route('/actualizar/<int:cancha_id>', methods=['PUT'])
@jwt_required()
def actualizar_cancha(cancha_id):
    """
    Actualiza la información de una cancha específica si el usuario tiene permisos de administrador.
    """
    user_id = get_jwt_identity()  # Obtener el ID del usuario desde el JWT
    
    # Verificar si el usuario tiene rol de administrador
    if not es_admin(user_id):
        return jsonify({"msg": "Acción no permitida, necesitas privilegios de administrador"}), 403

    try:
        data = request.get_json()
        nuevo_tipo_cancha = data.get('tipo_cancha')
        nueva_cantidad = data.get('cantidad')
        nuevo_precio = data.get('precio')

        # Validar los datos proporcionados
        if not nuevo_tipo_cancha or nueva_cantidad is None or nuevo_precio is None:
            return jsonify({"msg": "Datos incompletos: se requiere tipo_cancha, cantidad y precio."}), 400

        if nueva_cantidad < 0 or nuevo_precio < 0:
            return jsonify({"msg": "Cantidad y precio no pueden ser negativos."}), 400

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si la cancha existe
        cursor.execute("SELECT * FROM canchas WHERE id = %s", (cancha_id,))
        cancha = cursor.fetchone()

        if not cancha:
            cursor.close()
            conexion.close()
            return jsonify({"msg": "Cancha no encontrada"}), 404

        # Actualizar la cancha
        query = """
            UPDATE canchas 
            SET tipo_cancha = %s, cantidad = %s, precio = %s
            WHERE id = %s
        """
        cursor.execute(query, (nuevo_tipo_cancha, nueva_cantidad, nuevo_precio, cancha_id))
        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({"msg": "Cancha actualizada exitosamente"}), 200

    except Exception as e:
        print(f"Error al actualizar la cancha: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500
