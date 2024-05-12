from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token
from flask_sqlalchemy import SQLAlchemy
import bcrypt

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
        """Handles get request for login page"""

        return render_template("login.html", localization=localization)

    @app.route("/login", methods=["POST"])
    def login_post():
        """Handles post requests for authorizations"""

        # extract inputs
        input_username = request.json.get("username", None)
        input_password = request.json.get("password", None)

        # check if fields are actually present
        if input_username is None:
            return jsonify({"msg": "Missing username"}), 422

        # check if fields are actually present 2
        if input_password is None:
            return jsonify({"msg": "Missing password"}), 422

        # find user with this exact same username
        result: models.User = db.session.execute(
            db.select(models.User).filter_by(username=input_username)
        ).scalar_one_or_none()

        # user doesn't exist, return error
        if result is None:
            return jsonify({"msg": "Bad credentials"}), 401

        # wrong password, return error
        if not bcrypt.checkpw(bytes(input_password, "utf-8"), result.passhash):
            return jsonify({"msg": "Bad credentials"}), 401

        # everything is ok, generate token and response
        response = make_response(redirect("login", 302))
        access_token = create_access_token(identity=str(result.id))
        set_access_cookies(response, access_token)

        return response

    return app
