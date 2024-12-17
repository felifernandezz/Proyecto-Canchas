import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_default')

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Bahiachivo124')  # Cambia por tu contraseña
    MYSQL_DB = os.getenv('MYSQL_DB', 'sistema_reservas')

class ProductionConfig(Config):
    DEBUG = False
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
