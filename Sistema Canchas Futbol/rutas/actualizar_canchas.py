from flask import Blueprint, jsonify, request
from extensiones import db
from modelos.cancha import Cancha

actualizar_canchas_bp=Blueprint("actualizar_canchas_bp", __name__)

@actualizar_canchas_bp.route('/<int:cancha_id>',methods=['PUT'])
def actualizar_cancha(cancha_id):
    cancha=Cancha.query.get_or_404(cancha_id)
    data=request.get_json()

    cancha.tipo_cancha = data.get('tipo_cancha', cancha.tipo_cancha)
    cancha.cantidad = data.get('cantidad', cancha.cantidad)

    db.session.commit()

    return jsonify({"msg": "Cancha actualizada exitosamente"}), 200