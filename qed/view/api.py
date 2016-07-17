from flask import Blueprint, abort, jsonify, request

from flask_login import current_user

from markdown import markdown as markdown_converter

from pony.orm import commit, db_session

from ..csrf import csrf
from ..models import Character

api = Blueprint("api", "api")


@csrf.exempt
@api.route("markdown/", methods=("POST",))
def markdown():
    text = request.form.get("text")
    if text is None:
        abort(400)
    return jsonify(dict(html=markdown_converter(text)))


@csrf.exempt
@api.route("character/<int:eid>/", methods=("POST", "DELETE"))
@db_session
def character(eid):
    entity = Character.get_or_404(eid)
    if entity.player.id != current_user.id:
        abort(403)

    if request.method == "POST":
        if request.args.get("action") == "set-main":
            entity.player.main = entity
            commit()
        else:
            abort(400)
    else:
        if entity.player.main.id == entity.id:
            abort(400)
        else:
            entity.delete()
            commit()
    return "ok"
