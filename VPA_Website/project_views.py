from flask import Blueprint, render_template, redirect, jsonify, request, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, \
    unset_jwt_cookies, get_current_user
import bcrypt


def create_project_blueprint(db, models):
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
            project_obj=result
        )

    @project_blueprint.route("/project", methods=["POST"])
    @jwt_required(optional=True)
    def project_post():
        """Creates news posts"""

        # extract inputs
        input_user = get_jwt_identity()
        input_name = request.json.get("name", None)
        input_desc = request.json.get("desc", None)

        if input_user is None:
            return jsonify({"msg": "Missing credentials"}), 401

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

        response = make_response(jsonify({}), 201)
        response.headers["Location"] = "/project/{}".format(str(new_project.id))

        return response

    @project_blueprint.route("/project/<int:project_id>/category", methods=["POST"])
    @jwt_required(optional=True)
    def category_post(project_id):
        """Creates category for specified project"""

        input_user = get_jwt_identity()
        input_name = request.json.get("name", None)

        # is someone even logged
        if input_user is None:
            return jsonify({"msg": "Missing credentials"}), 401

        project_obj = db.session.execute(
            db.select(models.Project).filter_by(id=project_id)
        ).scalar_one_or_none()

        # does project even exists
        if project_obj is None:
            return jsonify({"msg": "Project doesn't exist"}), 404

        # does current user owns the project
        if project_obj.user_id != input_user:
            jsonify({"msg": "Wrong credentials"}), 403

        # is there category with the same name already?
        if len([item for item in project_obj.categories if item.name == input_name]) > 0:
            return jsonify({"msg": "Category with this name already exists"}), 409

        new_category = models.ItemCategory(
            project_id=project_id,
            name=input_name
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({}), 201

    @project_blueprint.route("/category/<int:category_id>/item", methods=["POST"])
    @jwt_required(optional=True)
    def item_post(category_id):
        """Creates new item in specified category"""

        input_user = int(get_jwt_identity())
        input_name = request.json.get("name", None)

        # is input name even there?
        if input_name is None:
            return jsonify({"msg": "Missing username"}), 422

        # is someone even logged?
        if input_user is None:
            return jsonify({"msg": "Missing credentials"}), 401

        category_obj = db.session.execute(
            db.select(models.ItemCategory).filter_by(id=category_id)
        ).scalar_one_or_none()

        # does category even exists
        if category_obj is None:
            return jsonify({"msg": "Category doesn't exist"}), 404

        # does current user owns the category
        if category_obj.my_project.user_id != input_user:
            return jsonify({"msg": "Wrong credentials"}), 403

        # is there item with the same name already?
        if len([item for item in category_obj.items if item.name == input_name]) > 0:
            return jsonify({"msg": "Item with this name already exists"}), 409


        new_item = models.Item(
            category_id=category_id,
            name=input_name
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({}), 201

    @project_blueprint.route("/item/<int:item_id>", methods=["PUT"])
    @jwt_required(optional=True)
    def item_put(item_id):
        """Changes data of item, in most cases category id"""

        new_group_id = int(request.json.get("group_id", None))
        if new_group_id is None:
            return jsonify({"msg": "Missing group id"}), 422

        item_obj = db.session.execute(
            db.select(models.Item).filter_by(id=item_id)
        ).scalar_one_or_none()

        if item_obj is None:
            return jsonify({"msg": "Requested item doesn't exist"}), 404

        item_obj.category_id = new_group_id
        db.session.commit()

        return jsonify({}), 200

    @project_blueprint.route("/item/<int:item_id>", methods=["DELETE"])
    @jwt_required(optional=True)
    def item_delete(item_id):
        item_obj = db.session.execute(
            db.select(models.Item).filter_by(id=item_id)
        ).scalar_one_or_none()

        if item_obj is None:
            return jsonify({"msg": "Requested item doesn't exist"}), 404

        db.session.delete(item_obj)
        db.session.commit()

        return jsonify({}), 200


    return project_blueprint
