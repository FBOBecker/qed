from uuid import uuid4

from os.path import splitext, abspath

from flask import Blueprint, flash, render_template, redirect, url_for

from flask_login import current_user

from pony.orm import db_session, commit

from ..forms import FileForm

profile = Blueprint("profile", "profile")


@profile.route("/")
def index():
    return render_template("profile/index.html")


@profile.route("picture/", methods=("GET", "POST"))
@db_session
def picture():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        _, ext = splitext(file.filename)
        uuid = uuid4()
        filename = "{}{}".format(uuid, ext)
        file.save(abspath("qed/static/profile_pictures/" + filename))
        current_user.forum.picture = filename
        commit()
        flash("File uploaded", "success")
        return redirect(url_for("profile.picture"))

    return render_template("profile/picture.html", form=form)
