import eventlet
eventlet.monkey_patch(thread=True, time=True)

from flask import Flask
from config import Config
from extensions import db, migrate, cache, mail, jwt, cors, socketio
from routes import stock_blueprint, auth_blueprint




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app,resources={r"^/":{"origins":'*'}})
    
    # Register blueprints
    app.register_blueprint(stock_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app


if __name__ == '__main__':
    app = create_app()
    socketio.init_app(app,cors_allowed_origins="*")
    socketio.run(app,host="0.0.0.0",debug=True)

