from flask import Blueprint, jsonify

items_blueprint = Blueprint("items_blueprint", __name__)


@items_blueprint.route('/posts', methods=["GET"])
def get_posts():
    return "Posts"


@items_blueprint.route('/post', methods=['POST'])
def create_post():
    return jsonify({"info": "Post was created"})
