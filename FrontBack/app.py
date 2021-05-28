from flask import Flask
from auth.auth import auth as auth_blueprint
from core.main import main as main_blueprint
from models import db,Admins
from flask_login import LoginManager

app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = '2021secrete'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@db/Clientes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Clientes'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#pasamos la configuración de la app a sqlalchemy y guardamos el objeto para acceder a la base

# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(AdminID):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Admins.query.get(int(AdminID))
