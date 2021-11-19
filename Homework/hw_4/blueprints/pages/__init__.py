from flask import Blueprint
from .main import main_page_blueprint
from .other import other_page_blueprint

pages_blueprint = Blueprint("pages_blueprint", __name__, url_prefix="/pages")
pages_blueprint.register_blueprint(main_page_blueprint)
pages_blueprint.register_blueprint(other_page_blueprint)
