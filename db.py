from pony.orm import commit

from qed.models import *
from qed.enums import *


def fill():
    c = Character(name="Apophänie", realm=Realm.Veklor, spec=Spec.Heal, cls=Class.Paladin)
    c2 = Character(name="Wombatz", realm=Realm.Veklor, spec=Spec.Heal, cls=Class.Paladin)
    commit()
    u = User(nick_name="Wombatz", password="lol", is_admin=True, is_active=True, main=c)
    u.characters.add(c2)
    ForumUser(user=u)
    Category(title="Announcements")
    Category(title="General")
    Category(title="Off Topic")
    classes = Category(title="Classes")
    for _, value in Class.items()[1:]:
        Category(title=value.capitalize(), parent=classes)
    commit()


def drop():
    db.drop_all_tables(with_all_data=True)
