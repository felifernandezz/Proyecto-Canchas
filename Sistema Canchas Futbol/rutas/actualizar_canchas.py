from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.cancha import Cancha
from modelos.usuarios import Usuario
from extensiones import db

actualizar_canchas_bp = Blueprint('actualizar_canchas_bp', __name__)

def es_admin(user_id):
    # Aquí puedes verificar el rol de administrador en tu base de datos
    # Si el usuario tiene rol "admin", se permite la operación
    usuario = Usuario.query.get(user_id)
    return usuario.rol == 'admin'

@actualizar_canchas_bp.route('/actualizar/<int:cancha_id>', methods=['PUT'])
@jwt_required()
def actualizar_cancha(cancha_id):
    user_id = get_jwt_identity()  # Obtener el ID del usuario desde el JWT
    
    # Verificar si el usuario tiene rol de administrador
    if not es_admin(user_id):
        return jsonify({"msg": "Acción no permitida, necesitas privilegios de administrador"}), 403

    cancha = Cancha.query.get_or_404(cancha_id)
    data = request.get_json()

    cancha.tipo_cancha = data.get('tipo_cancha', cancha.tipo_cancha)
    cancha.cantidad = data.get('cantidad', cancha.cantidad)

    db.session.commit()

    return jsonify({"msg": "Cancha actualizada exitosamente"}), 200
