from re import findall

from flask import abort

from pony.orm import Database
from pony.orm import ObjectNotFound

__all__ = ["db"]


db = Database()


class EntityMixin:
    pattern = "{class}[{id}]"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        data = {"class": self.__class__.__name__}
        for key in findall(r"\{([a-z_]+)\}", self.pattern):
            if key != "class":
                data[key] = getattr(self, key)
        return self.pattern.format(**data)

    @classmethod
    def get_or_404(cls, eid):
        try:
            return cls[eid]
        except ValueError:
            abort(400)
        except ObjectNotFound:
            abort(404)
