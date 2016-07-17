from flask import abort

from pony.orm import Database
from pony.orm import ObjectNotFound

from re import findall

__all__ = ["db"]


db = Database()


class EntityMixin:
    str = "{class_name}[{id}]"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        data = {"class": self.__class__.__name__}
        for key in findall(r"\{([a-z_]+)\}", self.str):
            data[key] = getattr(self, key)
        return self.str.format(**data)

    @classmethod
    def get_or_404(cls, eid):
        try:
            return cls[eid]
        except ValueError:
            abort(400)
        except ObjectNotFound:
            abort(404)
