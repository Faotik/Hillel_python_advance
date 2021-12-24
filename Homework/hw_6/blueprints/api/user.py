from flask import Blueprint, jsonify, redirect
from core.models.userModels import RegistrationModel
from .utility import get_input, get_current_user
from core.db import get_connection
from crud.user import UserCRUD

user_crud = UserCRUD()
user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route('/registration', methods=["POST"])
def user_registration():
    data = get_input(RegistrationModel)

    with get_connection() as conn:
        user_crud.create(conn, data)

    return jsonify({"info": "OK"}), 201


@user_blueprint.route('/login', methods=['GET'])
def login():
    data = get_current_user()

    with get_connection() as conn:
        user_crud.authenticate(conn, data)

    return jsonify({"info": "OK"})


@user_blueprint.route('/user', methods=['GET'])
def user():
    data = get_current_user()

    with get_connection() as conn:
        user_data = user_crud.user_data_by_login(conn, data.username)

    return jsonify({"info": f"{user_data}"})


@user_blueprint.route('/user/<string:login>', methods=['GET'])
def user_by_login(login: str):
    with get_connection() as conn:
        user_data = user_crud.user_data_by_login(conn, login)

    return jsonify({"info": f"{user_data}"})


@user_blueprint.route('/follow/<string:follow_login>', methods=['POST'])
def follow(follow_login: str):
    data = get_current_user()
    with get_connection() as conn:
        user_data = user_crud.follow(conn, data.username, follow_login)

    return jsonify({"info": "OK"})


@user_blueprint.route('/follow/<string:follow_login>', methods=['DELETE'])
def unfollow(follow_login: str):
    data = get_current_user()
    with get_connection() as conn:
        user_data = user_crud.unfollow(conn, data.username, follow_login)

    return jsonify({"info": "OK"})

@user_blueprint.route('/follows/<string:login>', methods=['GET'])
def user_follows(login: str):
    with get_connection() as conn:
        user_data = user_crud.get_follows(conn, login)

    return jsonify({"info": f"{user_data}"})


@user_blueprint.route('/follows', methods=['GET'])
def follows():
    data = get_current_user()

    return redirect(f"./follows/{data.username}", 302)


@user_blueprint.route('/followers/<string:login>', methods=['GET'])
def user_follower(login: str):
    with get_connection() as conn:
        user_data = user_crud.get_follower(conn, login)

    return jsonify({"info": f"{user_data}"})
