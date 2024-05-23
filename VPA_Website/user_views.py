from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_current_user
import bcrypt


def create_user_blueprint(db, models):
    user_blueprint = Blueprint(
        "user_blueprint",
        __name__,
        template_folder="templates"
    )

    @user_blueprint.route("/user/<int:user_id>", methods=["GET"])
    @jwt_required(optional=True)
    def user_by_id_get(user_id):
        """Returns profile of user that has passed id"""

        # find user with this id
        result: models.User = db.session.execute(
            db.select(models.User).filter_by(id=user_id)
        ).scalar_one_or_none()

        return render_template(
            "user_profile.html",
            auth_user=get_current_user(),
            user_obj=result
        )

    @user_blueprint.route("/user", methods=["POST"])
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

    return user_blueprint
