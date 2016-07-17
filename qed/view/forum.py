from pony.orm import commit, db_session, select

from flask import Blueprint, flash, redirect, render_template, url_for

from ..forms import NewPost, NewThreadForm
from ..models import Category, Thread, Post

forum = Blueprint("forum", "forum")


@forum.route("/")
@db_session
def index():
    toplevel = select(cat for cat in Category if cat.parent is None)
    return render_template("forum/categories.html", categories=toplevel)


@forum.route("<int:eid>/", methods=("GET", "POST"))
@db_session
def category(eid):
    entity = Category.get_or_404(eid)
    if entity.children:
        return render_template("forum/categories.html", entity=entity, categories=entity.children)
    form = NewThreadForm()
    if form.validate_on_submit():
        t = Thread(title=form.title.data, parent=entity)
        Post(parent=t, text=form.text.data)
        commit()
        return redirect(url_for("forum.thread", eid=t.id))
    return render_template("forum/threads.html", entity=entity, threads=entity.threads, form=form)


@forum.route("thread/<int:eid>/", methods=("GET", "POST"))
@db_session
def thread(eid):
    entity = Thread.get_or_404(eid)
    form = NewPost()
    if form.validate_on_submit():
        if entity.is_locked:
            flash("This thread is locked, you cannot create new posts!", "danger")
        else:
            p = Post(parent=entity, text=form.text.data)
            commit()
            return redirect(url_for("forum.thread", eid=eid, _anchor="post-" + str(p.id)))
    return render_template("forum/posts.html", thread=entity, form=form)
