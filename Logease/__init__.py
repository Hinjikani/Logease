from flask import Flask
from os import path
from Logease.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from Logease.main.routes import main
    app.register_blueprint(main)
    return app