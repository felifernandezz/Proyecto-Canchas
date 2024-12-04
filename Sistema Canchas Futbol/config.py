import os

# Configuración general
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_default')  # Clave para proteger la app (JWT, CSRF, etc.)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva notificaciones de cambios (mejora rendimiento)

# Configuración para entorno de desarrollo
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql://root:reservas@127.0.0.1:3306/sistema_reservas'
    )  # Cambia los datos según tu base de datos local

# Configuración para entorno de producción
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # La URL de la base de datos se define en las variables de entorno

# Diccionario para seleccionar configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
