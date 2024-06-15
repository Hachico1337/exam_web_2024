from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from database.models import *
from resources.actions import register_actions
from resources.errors import Errors


def create_app(config):
    """
    создаем приложение
    """
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    CORS(app)
    Marshmallow(app)
    register_actions(app)
    Errors(app)
    return app
