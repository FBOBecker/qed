from pony.orm import Optional, Required

from .base import db
from ..enums import Specialization


class Character(db.Entity):
    name = Required(str)
    _spec = Required(int)
    player = Optional("User")

    def __init__(self, **kwargs):
        kwargs["_spec"] = kwargs.pop("spec").value
        super().__init__(**kwargs)

    @property
    def spec(self):
        return Specialization(self._spec)

    @spec.setter
    def spec(self, value):
        self._spec = value.value
