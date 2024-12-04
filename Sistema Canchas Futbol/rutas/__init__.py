from flask import Blueprint
from .actualizar_canchas import actualizar_canchas_bp
from .cancelar_reserva import cancelar_reserva_bp
from .canchas_disponibles import canchas_disponibles_bp
from .reservas_cancha import reservar_cancha_bp

# Registrar los blueprints
main_bp = Blueprint('main', __name__)

main_bp.register_blueprint(actualizar_canchas_bp, url_prefix='/actualizar_canchas')
main_bp.register_blueprint(cancelar_reserva_bp, url_prefix='/cancelar_reserva')
main_bp.register_blueprint(canchas_disponibles_bp, url_prefix='/canchas_disponibles')
main_bp.register_blueprint(reservar_cancha_bp, url_prefix='/reservar_cancha')
