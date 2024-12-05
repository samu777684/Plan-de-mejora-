from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicialización de la base de datos
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/biblioteca'  # Cambia el nombre de la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos y migraciones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración de JWT
    app.config["JWT_SECRET_KEY"] = 'clavesecreta'
    jwt = JWTManager(app)

    # Habilitar CORS
    CORS(app)

    # Configuración del puerto de ejecución
    app.config['FLASK_RUN_PORT'] = 5000  

    return app
