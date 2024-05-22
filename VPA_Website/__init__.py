from flask import Flask, render_template, request, jsonify, make_response, redirect, Response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_current_user
from flask_sqlalchemy import SQLAlchemy
import bcrypt


class Localization:
    def __getitem__(self, name):
        return name


def create_app(app_config, initialize_db=False):
    app = Flask(
        __name__,
        static_url_path="",
        static_folder="static"
    )
    jwt = JWTManager()

    app.config.from_object(app_config)
    jwt.init_app(app)

    import VPA_Website.models as models
    db = models.db
    db.init_app(app)

    # initialize database tables
    if initialize_db:
        with app.app_context():
            db.create_all()

    # load localization (implement translations
    localization = Localization()

    @jwt.unauthorized_loader
    def handle_missing_auth_cookie(message):
        """Handler for requests with missing cookie"""

        return redirect("/login", 302)

    @jwt.invalid_token_loader
    def handle_invalid_auth_cookie(message):
        """Handler for invalid tokens"""

        response = make_response(redirect('/login'))
        unset_jwt_cookies(response)
        return response, 302

    @jwt.user_lookup_loader
    def handle_user_load(jwt_header, jwt_payload):
        """Finds user with same id as is in cookie"""

        user_id = jwt_payload["sub"]

        return db.session.execute(
            db.select(models.User).filter_by(id=user_id)
        ).scalar_one_or_none()

    # register blueprints
    from VPA_Website.auth_views import create_auth_blueprint
    app.register_blueprint(create_auth_blueprint(db, models, localization))

    from VPA_Website.user_views import create_user_blueprint
    app.register_blueprint(create_user_blueprint(db, models, localization))

    from VPA_Website.project_views import create_project_blueprint
    app.register_blueprint(create_project_blueprint(db, models, localization))

    @app.route("/")
    @app.route("/index")
    @jwt_required(optional=True)
    def index_get():

        return render_template("index.html", auth_user=get_current_user(), localization=localization)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected_get():
        return "<h1>Successful login</h1>"







    return app
