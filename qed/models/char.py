from pony.orm import Optional, Required

from .base import EntityMixin, db
from ..enums import Class, Realm, Spec


class Character(EntityMixin, db.Entity):
    name = Required(str)
    _realm = Required(int)
    _spec = Required(int)
    _class = Required(int)
    player = Optional("User")

    def __init__(self, **kwargs):
        kwargs["_spec"] = kwargs.pop("spec").value
        kwargs["_realm"] = kwargs.pop("realm").value
        kwargs["_class"] = kwargs.pop("cls").value
        super().__init__(**kwargs)

    @property
    def spec(self):
        return Spec(self._spec)

    @spec.setter
    def spec(self, value):
        self._spec = value.value

    @property
    def realm(self):
        return Realm(self._realm)

    @realm.setter
    def realm(self, value):
        self._realm = value.value

    @property
    def cls(self):
        return Class(self._class)

    @cls.setter
    def cls(self, value):
        self._class = value.value
