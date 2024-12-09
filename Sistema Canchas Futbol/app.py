# app.py
from flask_cors import CORS #habria que instalar " pip install flask-cors " 
from flask import Flask,render_template
from flask_migrate import Migrate
from extensiones import db, jwt  # Importamos db y jwt desde extensiones.py
from rutas import main_bp

app = Flask(__name__)
CORS(app)

# Configuración de base de datos y JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/sistema_reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'

# Inicializar extensiones
db.init_app(app)  # Usamos el método init_app para inicializar db
jwt.init_app(app)

# Registrar los blueprints
app.register_blueprint(main_bp)

@app.route('/reservas', methods=['GET'])
def mostrar_reservas():
    return render_template('reservas.html')

if __name__ == "__main__":
    app.run(debug=True)
