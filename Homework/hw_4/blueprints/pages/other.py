from flask import Blueprint, render_template

other_page_blueprint = Blueprint("other_page_blueprint", __name__)


@other_page_blueprint.route('/posts', methods=["GET"])
def posts():
    return render_template("posts.html")


@other_page_blueprint.route('/profile', methods=["GET"])
def profile():
    return render_template("profile.html")
