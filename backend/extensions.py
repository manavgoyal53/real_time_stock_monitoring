from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO


jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
mail = Mail()
cors = CORS()
socketio = SocketIO()
