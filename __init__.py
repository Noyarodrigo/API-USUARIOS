from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2021secrete'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@db/Clientes'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    #pasamos la configuración de la app a sqlalchemy y guardamos el objeto para acceder a la base
    db = SQLAlchemy(app)

    # blueprint for auth routes in our app
    from .auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .core.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
