from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_user, logout_user

from pony.orm import db_session

from ..forms import LoginForm, RegisterForm
from ..models import User

user = Blueprint("user", "user")


@user.route("/")
def index():
    return render_template("main/divert.html")


@user.route("login/", methods=("GET", "POST"))
@db_session
def login():
    form = LoginForm()
    if form.validate_on_submit():
        potential_user = User.get(nick_name=form.nick_name.data)
        if potential_user is not None and potential_user.password == form.password.data:
            login_user(potential_user)
            flash("Logged in", "success")
            return redirect(url_for(request.args.get("next", "main.index")))
        else:
            flash("Fail", "danger")
    flash("yolo", "warning")
    return render_template("user/login.html", form=form)


@user.route("logout/", methods=["POST"])
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for("main.index"))


@user.route("register/")
@db_session
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template("user/register.html")
