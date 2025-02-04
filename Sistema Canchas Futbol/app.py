
from flask_cors import CORS
from flask import Flask, render_template, jsonify
from extensiones import obtener_conexion, jwt  
from rutas import main_bp
from config import config  # Importar configuraciones desde config.py

# Crear instancia de Flask
app = Flask('_name_', static_folder='static', template_folder='templates')
CORS(app)
app.secret_key = "advpjsh"

# Cargar configuración según el entorno
env = 'development'  # Cambiar a 'production' en producción
app.config.from_object(config[env])

# Inicializar JWT
jwt.init_app(app)

# Registrar blueprints
app.register_blueprint(main_bp)
@app.route('/')
def home():
    return render_template('index.html')  # Carga index.html

@app.route('/reserva', methods=['GET'])
def mostrar_reservas():
    return render_template('calendario_reserva.html')

# Conexión de prueba a la base de datos (puedes eliminarla después de verificar)
@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conexion.close()
        return jsonify({"msg": "Conexión exitosa a la base de datos", "result": result}), 200
    except Exception as e:
        return jsonify({"msg": "Error al conectar a la base de datos", "error": str(e)}), 500

if __name__ == "_main_":
    app.run(debug=app.config['DEBUG'])