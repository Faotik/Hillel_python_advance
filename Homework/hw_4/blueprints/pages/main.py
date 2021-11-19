from flask import Blueprint, render_template

main_page_blueprint = Blueprint("main_page_blueprint", __name__)


@main_page_blueprint.route('/index', methods=["GET"])
def index():
    return render_template("index.html")


@main_page_blueprint.route('/registration', methods=["GET"])
def registration():
    return render_template("registration.html")
