from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, DevelopmentConfig, TestingConfig
import os

db = SQLAlchemy()
migrate = Migrate()
configurations = {
    'default': Config,
    'DevelopmentConfig': DevelopmentConfig,
    'TestingConfig': TestingConfig
}


def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or os.environ.get(
        'FLASK_CONFIG', 'DevelopmentConfig')
    app.config.from_object(configurations[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    from app import views
    views.register(app)
    return app
