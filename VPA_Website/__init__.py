from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


class Localization:
    def __getitem__(self, name):
        return name

def create_app(app_config):
    app = Flask(__name__)
    db = SQLAlchemy()
    jwt = JWTManager()

    app.config.from_object(app_config)
    db.init_app(app)
    jwt.init_app(app)

    from VPA_Website.models import create_models
    models = create_models(db)

    # load localization (implement translations
    localization = Localization()

    @app.route("/")
    @app.route("/index")
    def index_get():
        return render_template("index.html", localization=localization)

    @app.route("/login", methods=["GET"])
    def login_get():
        """Handles login page"""
        return render_template("login.html", localization=localization)


    return app
