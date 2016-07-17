from pony.orm import Optional, Required, Set

from werkzeug.security import check_password_hash, generate_password_hash

from .base import db, EntityMixin


class PasswordEq:
    def __init__(self, hash_):
        self._hash = hash_

    def __eq__(self, other):
        return check_password_hash(self._hash, other)

    def __ne__(self, other):
        return not self.__eq__(other)


class User(EntityMixin, db.Entity):
    nick_name = Required(str, unique=True)
    _password_hash = Required(str)
    characters = Set("Character")
    is_active = Required(bool)
    is_admin = Required(bool)

    is_authenticated = True
    is_anonymous = False

    forum = Optional("ForumUser")

    def __init__(self, **kwargs):
        kwargs["is_active"] = kwargs.get("is_active", False)
        kwargs["_password_hash"] = generate_password_hash(kwargs.pop("password"))
        super().__init__(**kwargs)

    @property
    def password(self):
        return PasswordEq(self._password_hash)

    @password.setter
    def password(self, value):
        self._password_hash = generate_password_hash(value)

    def get_id(self):
        return str(self.id)

    str = "User {nick_name} {id}"
