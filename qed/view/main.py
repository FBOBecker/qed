from flask import Blueprint, render_template


main = Blueprint("main", "main")


@main.route("/")
def index():
    return render_template("main/divert.html")
