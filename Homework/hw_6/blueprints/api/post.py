from flask import Blueprint, jsonify
from core.models.postModel import CreatePostModel, RawCreatePostModel
from .utility import get_input, get_current_user
from core.db import get_connection
from crud.post import PostCRUD

post = PostCRUD()
post_blueprint = Blueprint("post_blueprint", __name__)


@post_blueprint.route('/post', methods=["POST"])
def create_post():
    data = get_input(RawCreatePostModel)
    user_data = get_current_user()

    with get_connection() as conn:
        post.create(conn, CreatePostModel(
            title=data.title, description=data.description, creater=user_data.username))

    return jsonify({"info": "OK"}), 201


@post_blueprint.route('/post/<string:id>', methods=["DELETE"])
def delete_post(id: str):
    user_data = get_current_user()

    with get_connection() as conn:
        post.delete(conn, id, user_data.username)

    return jsonify({"info": "OK"})


@post_blueprint.route('/posts', methods=["GET"])
def get_your_posts():
    user_data = get_current_user()

    with get_connection() as conn:
        posts = post.get(conn, user_data.username)

    return jsonify([post.dict() for post in posts])


@post_blueprint.route('/follows_posts', methods=["GET"])
def get_follows_posts():
    user_data = get_current_user()

    with get_connection() as conn:
        posts = post.get_follows_post(conn, user_data.username)

    return jsonify([post.dict() for post in posts])
