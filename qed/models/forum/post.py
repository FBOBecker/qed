from datetime import datetime

from flask_login import current_user

from pony.orm import Required

from ..base import db


class Post(db.Entity):
    parent = Required("Thread")
    author = Required("ForumUser")
    _timestamp = Required(datetime)

    text = Required(str)

    def __init__(self, **kwargs):
        kwargs.setdefault("author", current_user.forum)
        kwargs.setdefault("_timestamp", datetime.now())
        super().__init__(**kwargs)

    @property
    def when(self):
        return "2 hours ago"
