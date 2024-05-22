from flask import Flask, render_template, request, jsonify, make_response, redirect, Response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
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

        response = make_response(redirect('/signup'))
        unset_jwt_cookies(response)
        return response, 302

    @app.route("/")
    @app.route("/index")
    def index_get():
        return render_template("index.html", localization=localization)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected_get():
        return "<h1>Successful login</h1>"

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
        response = make_response(jsonify("{}"), 200)
        access_token = create_access_token(identity=str(result.id))
        set_access_cookies(response, access_token)

        return response

    @app.route("/user/<int:user_id>", methods=["GET"])
    def user_by_id_get(user_id):
        """Returns profile of user that has passed id"""

        # find user with this id
        result: models.User = db.session.execute(
            db.select(models.User).filter_by(id=user_id)
        ).scalar_one_or_none()

        return render_template("user_profile.html", localization=localization, user_obj=result)

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

        return render_template("register.html", localization=localization)



    return app
