from pony.orm import commit

from qed.models import *


CLASSES = """
    mage priest warlock rogue druid monk shaman hunter paladin deathknight warrior
""".split()


def fill():
    u = User(nick_name="Wombatz", password="lol", is_admin=True, is_active=True)
    ForumUser(user=u)
    Category(title="Announcements")
    Category(title="General")
    Category(title="Off Topic")
    classes = Category(title="Classes")
    for cls in CLASSES:
        Category(title=cls.capitalize(), parent=classes)
    commit()


def drop():
    db.drop_all_tables(with_all_data=True)
