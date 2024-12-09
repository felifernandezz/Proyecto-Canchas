from flask_cors import CORS
from flask import Flask, render_template
from flask_migrate import Migrate
from extensiones import db, jwt
from rutas import main_bp
from config import config  # Importar configuraciones desde config.py

# Crear instancia de Flask
app = Flask(__name__)
CORS(app)

# Cargar configuración según el entorno
env = 'development'  # Cambiar a 'production' en producción
app.config.from_object(config[env])

# Inicializar extensiones
db.init_app(app)
jwt.init_app(app)

# Inicializar migraciones
migrate = Migrate(app, db)

# Registrar blueprints
app.register_blueprint(main_bp)

@app.route('/reservas', methods=['GET'])
def mostrar_reservas():
    return render_template('reservas.html')

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
