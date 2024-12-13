from flask import Blueprint, jsonify
from extensiones import db
from modelos.cancha import Cancha

canchas_disponibles_bp = Blueprint('canchas_disponibles_bp', __name__)

@canchas_disponibles_bp.route('/tipos', methods=['GET'])
def obtener_tipos_canchas():
    canchas = Cancha.query.all()
    tipos_canchas = [{"tipo_cancha": cancha.tipo_cancha, "cantidad": cancha.cantidad} for cancha in canchas]
    return jsonify(tipos_canchas),200

@canchas_disponibles_bp.route('/cantidad/<int:cancha_id>', methods=['GET'])
def obtener_cantidad_de_un_tipoCancha(cancha_id):
        # Busca la cancha por su ID
    cancha = Cancha.query.get(cancha_id)
    if not cancha:
        return jsonify({"error": "No se encontró una cancha con ese ID"}), 404

    # Devuelve la cantidad de canchas disponibles para ese tipo
    return jsonify({
        "tipo_cancha": cancha.tipo_cancha,
        "cantidad_disponible": cancha.cantidad
    }), 200