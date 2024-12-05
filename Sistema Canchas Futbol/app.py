# app.py
from flask import Flask
from flask_migrate import Migrate
from extensiones import db, jwt  # Importamos db y jwt desde extensiones.py
from rutas import main_bp

app = Flask(__name__)

# Configuración de base de datos y JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/sistema_reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'

# Inicializar extensiones
db.init_app(app)  # Usamos el método init_app para inicializar db
jwt.init_app(app)

# Registrar los blueprints
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
