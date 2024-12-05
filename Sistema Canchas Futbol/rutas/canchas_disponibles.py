from flask import Blueprint, jsonify
from extensiones import db
from modelos.cancha import Cancha

canchas_disponibles_bp = Blueprint('canchas_disponibles_bp', __name__)

@canchas_disponibles_bp.route('/tipos', methods=['GET'])
def obtener_tipos_canchas():
    canchas = Cancha.query.all()
    tipos_canchas = [{"tipo_cancha": cancha.tipo_cancha, "cantidad": cancha.cantidad} for cancha in canchas]
    return jsonify(tipos_canchas),200
