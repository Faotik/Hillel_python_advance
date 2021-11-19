from flask import Blueprint, request, jsonify
import pydantic
from pydantic import BaseModel
from typing import Optional

user_blueprint = Blueprint("user_blueprint", __name__)


class UserModel(BaseModel):
    login: str
    password: str
    items: Optional[list]


# {
#     "login": "Some name",
#     "password": "Some password"
# }

@user_blueprint.route('/login', methods=["POST"])
def user_login():
    try:
        data = UserModel(**request.json)
    except pydantic.error_wrappers.ValidationError:
        return jsonify({"info": "Invalid value format"}), 403
    else:
        return jsonify({"info": "User was loggined"})


@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
    return "Users"
