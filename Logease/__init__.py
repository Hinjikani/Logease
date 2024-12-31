from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Logease.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from Logease.users.routes import users
    from Logease.main.routes import main
    from Logease.dashboard.routes import dash
    from Logease.armada.routes import armada
    from Logease.order.routes import order

    app.register_blueprint(armada)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(dash)
    app.register_blueprint(order)

    return app