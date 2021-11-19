from flask import Blueprint
from .user import user_blueprint
from .items import items_blueprint

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/api")
api_blueprint.register_blueprint(items_blueprint)
api_blueprint.register_blueprint(user_blueprint)
