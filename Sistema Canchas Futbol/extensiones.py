import mysql.connector
from flask_jwt_extended import JWTManager

# Configuración de conexión a MySQL usando mysql-connector
def obtener_conexion():
    conexion = mysql.connector.connect(
        host='127.0.0.1',  # Aquí va el host de MySQL
        user='root',  # Usuario de MySQL
        password='Bahiachivo124',  # Contraseña de MySQL
        database='sistema_reservas'  # Nombre de la base de datos
    )
    return conexion

# Inicialización de JWT
jwt = JWTManager()

# Inicialización de la conexión con la base de datos
def init_app(app):
    app.db = obtener_conexion()
    jwt.init_app(app)
