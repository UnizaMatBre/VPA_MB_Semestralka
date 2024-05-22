from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_current_user
import bcrypt


def create_project_blueprint(db, models, localization):
    project_blueprint = Blueprint(
        "project_blueprint",
        __name__,
        template_folder="templates"
    )

    @project_blueprint.route("/project/<int:project_id>")
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

    return project_blueprint
