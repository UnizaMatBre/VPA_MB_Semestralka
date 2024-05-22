from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, \
    unset_jwt_cookies, get_current_user
import bcrypt


def create_project_blueprint(db, models, localization):
    project_blueprint = Blueprint(
        "project_blueprint",
        __name__,
        template_folder="templates"
    )

    @project_blueprint.route("/project/<int:project_id>")
    @jwt_required(optional=True)
    def project_by_id_get(project_id):
        result = db.session.execute(
            db.select(models.Project).filter_by(id=project_id)
        ).scalar_one_or_none()

        return render_template(
            "project_profile.html",
            auth_user=get_current_user(),
            localization=localization,
            project_obj=result
        )

    @project_blueprint.route("/project", methods=["POST"])
    @jwt_required()
    def project_post():
        """Creates news posts"""

        # extract inputs
        input_user = get_jwt_identity()
        input_name = request.json.get("name", None)
        input_desc = request.json.get("desc", None)

        if input_name is None:
            return jsonify({"msg": "Missing project name"}), 422

        result = db.session.execute(
            db.select(models.Project).filter_by(user_id=input_user, name=input_name)
        ).scalar_one_or_none()

        if result is not None:
            return jsonify({"msg": "User already has project with this name"}), 409

        new_project = models.Project(
            user_id=input_user,
            name=input_name,
            description=input_desc
        )

        db.session.add(new_project)
        db.session.commit()

        response = make_response(jsonify("{}"), 201)
        response.headers["Location"] = "/project/{}".format(str(new_project.id))

        return response

    return project_blueprint
