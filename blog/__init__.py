from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b0b1bbb16052c8a2996fe0fde7e94543'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login ou crie sua conta para acessar essa pagina.'


from blog import routes
