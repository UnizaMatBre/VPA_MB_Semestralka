from flask import Blueprint


def create_auth_blueprint(db, models):
    auth_blueprint = Blueprint(
        "auth_blueprint",
        __name__
    )

    return auth_blueprint
