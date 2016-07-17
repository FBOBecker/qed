from flask import url_for

from pony.orm import Required, Set

from ..base import db


class ForumUser(db.Entity):
    user = Required("User")
    posts = Set("Post")
    _image_name = Required(str)

    def __init__(self, **kwargs):
        kwargs.setdefault("_image_name", "default.png")
        super().__init__(**kwargs)

    @property
    def picture(self):
        return url_for("static", filename="profile_pictures/{}".format(self._image_name))

    @picture.setter
    def picture(self, value):
        self._image_name = value

    def __str__(self):
        return "{} ({})".format(self.user.nick_name, self.user.main.name)
