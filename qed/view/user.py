from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_user, logout_user

from pony.orm import commit, db_session

from ..battlenet import character
from ..forms import LoginForm, RegisterForm
from ..models import Character, User

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


@user.route("register/", methods=("GET", "POST"))
@db_session
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nick = form.nick_name.data
        u = User.get(nick_name=nick)
        if u is not None:
            flash("The name {} is already taken!".format(nick), "danger")
        else:
            name = form.main_name.data
            realm = form.main_server
            response = character(name, realm.name)
            if response.status_code == 404:
                flash("Character {} does not exist on {}!".format(name, realm.title), "danger")
            elif response.status_code == 200:
                cls = response.json()["class"]
                c = Character(name=name, realm=realm, spec=form.main_spec, cls=cls)
                commit()
                User(nick_name=nick, password=form.password.data, main=c)
                commit()
                flash("Successfully registered!", "success")
            else:
                flash("Error {}".format(response.json()), "danger")
    return render_template("user/register.html", form=form)
