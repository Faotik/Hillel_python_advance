from flask import request
from pydantic import BaseModel
from core.errors.errors import AuthError
from core.db import get_connection
from crud.user import UserCRUD

user = UserCRUD()


def get_input(Model: type[BaseModel]) -> BaseModel:
    data = request.get_json(True)
    if data is None:
        raise AuthError("Json not found")

    return Model(**data)


def get_current_user() -> str:
    auth_data = request.authorization
    if auth_data is None:
        raise AuthError("Empty auth data")

    return auth_data
