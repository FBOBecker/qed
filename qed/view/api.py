from flask import Blueprint, abort, jsonify, request

from markdown import markdown as markdown_converter

from ..csrf import csrf


api = Blueprint("api", "api")


@csrf.exempt
@api.route("markdown/", methods=("POST",))
def markdown():
    text = request.form.get("text")
    if text is None:
        abort(400)
    return jsonify(dict(html=markdown_converter(text)))
