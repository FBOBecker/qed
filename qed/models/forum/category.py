from flask import url_for

from pony.orm import Optional, Required, Set

from ..base import EntityMixin, db


class Category(db.Entity, EntityMixin):
    title = Required(str)
    threads = Set("Thread")

    parent = Optional("Category")
    children = Set("Category")

    pattern = "Category {title}"

    @property
    def link(self):
        return url_for("forum.category", eid=self.id)
