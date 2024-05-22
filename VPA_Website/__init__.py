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

    @app.route("/")
    @app.route("/index")
    @jwt_required(optional=True)
    def index_get():

        return render_template("index.html", auth_user=get_current_user(), localization=localization)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected_get():
        return "<h1>Successful login</h1>"



    @app.route("/user/<int:user_id>", methods=["GET"])
    @jwt_required(optional=True)
    def user_by_id_get(user_id):
        """Returns profile of user that has passed id"""

        # find user with this id
        result: models.User = db.session.execute(
            db.select(models.User).filter_by(id=user_id)
        ).scalar_one_or_none()

        return render_template("user_profile.html", auth_user=get_current_user(), localization=localization, user_obj=result)

    @app.route("/user", methods=["POST"])
    def user_post():
        """Creates new user using data from request"""

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

        # user already exists, return error
        if result is not None:
            return jsonify({"msg": "User already exists"}), 409

        # generate password hash
        input_passhash = bcrypt.hashpw(
            password=bytes(input_password, "utf-8"),
            salt=bcrypt.gensalt()
        )

        # create user
        new_user = models.User(
            username=input_username,
            passhash=input_passhash
        )

        db.session.add(new_user)

        # create response
        response = make_response(jsonify("{}"), 201)
        response.headers["Location"] = "/user/" + str(new_user.id)

        db.session.commit()

        return response

    @app.route("/register", methods=["GET"])
    @jwt_required(optional=True)
    def register_get():
        """Renders registration page"""

        if get_jwt_identity() is not None:
            # TODO: Is 302 good here?
            return redirect("/index", 302)

        return render_template("register.html", auth_user=None, localization=localization)

    return app
