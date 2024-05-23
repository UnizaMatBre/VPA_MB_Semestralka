from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_current_user
import bcrypt


def create_auth_blueprint(db, models):
    auth_blueprint = Blueprint(
        "auth_blueprint",
        __name__,
        template_folder="templates"
    )

    @auth_blueprint.route("/login", methods=["GET"])
    @jwt_required(optional=True)
    def login_get():
        """Handles get request for login page"""

        print("test")

        if get_jwt_identity() is not None:
            # TODO: Is 302 good here?
            return redirect("/index", 302)

        return render_template("login.html", auth_user=None)

    @auth_blueprint.route("/login", methods=["POST"])
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

    @auth_blueprint.route("/logout", methods=["GET"])
    @jwt_required()
    def logout_get():
        """Logs out current user"""

        response = make_response(redirect('/index'))
        unset_jwt_cookies(response)
        return response, 302

    @auth_blueprint.route("/register", methods=["GET"])
    @jwt_required(optional=True)
    def register_get():
        """Renders registration page"""

        if get_jwt_identity() is not None:
            # TODO: Is 302 good here?
            return redirect("/index", 302)

        return render_template("register.html", auth_user=None)

    return auth_blueprint
