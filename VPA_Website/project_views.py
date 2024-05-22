from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_current_user
import bcrypt


def create_project_blueprint(db, models, localization):
    project_blueprint = Blueprint(
        "project_blueprint",
        __name__,
        template_folder="templates"
    )

    return project_blueprint
