import os

from flask import Flask
from extensions import db, login_manager


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    # ==========================================
    # CONFIGURATION
    # ==========================================

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "afit-football-2026"
    )

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================================
    # INITIALIZE EXTENSIONS
    # ==========================================

    db.init_app(app)
    login_manager.init_app(app)

    # ==========================================
    # IMPORT MODELS
    # ==========================================

    from models.user import User
    from models.team import Team
    from models.group import Group
    from models.match_event import MatchEvent
    from models.fixture import Fixture
    from models.player import Player
    from models.lineup import Lineup

    # ==========================================
    # REGISTER ROUTES
    # ==========================================

    from app.routes import register_routes

    register_routes(app)

    # ==========================================
    # CREATE DATABASE TABLES
    # ==========================================

    with app.app_context():

        db.create_all()

    return app
