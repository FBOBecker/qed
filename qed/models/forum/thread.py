from ..base import db, EntityMixin

from flask import url_for

from pony.orm import Required, Set


class Thread(EntityMixin, db.Entity):
    parent = Required("Category")
    posts = Set("Post")
    title = Required(str)
    is_sticky = Required(bool)
    is_locked = Required(bool)

    def __init__(self, **kwargs):
        kwargs.setdefault("is_sticky", False)
        kwargs.setdefault("is_locked", False)
        super().__init__(**kwargs)

    @property
    def link(self):
        return url_for("forum.thread", eid=self.id)
