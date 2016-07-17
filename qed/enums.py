from enum import Enum


class Int(int):
    def __new__(cls, int_value, *_):
        return int.__new__(cls, int_value)


class IntEnum(Int, Enum):
    @classmethod
    def items(cls):
        return [("", "")] + [(str(m.value), m.title) for m in cls]


class Spec(IntEnum):
    Heal = 1
    Tank = 2
    Melee = 3
    Ranged = 4

    @property
    def title(self):
        return self.name


class Class(IntEnum):
    Priest = 5, "mana"
    Mage = 8, "mana"
    Warlock = 9, "mana"
    Rogue = 4, "energy"
    Monk = 10, "energy"
    Druid = 11, "mana"
    DemonHunter = 3, "fel-shit"
    Shaman = 7, "mana"
    Hunter = 1, "focus"
    Paladin = 2, "mana"
    DeathKnight = 6, "runic-power"
    Warrior = 1, "rage"

    @property
    def title(self):
        return self.name

    def __init__(self, int_value, *args):
        Enum.__init__(int_value)
        self.power, = args


class Realm(IntEnum):
    Arthas = 1, "Arthas"
    Blutkessel = 2, "Blutkessel"
    Kelthuzad = 3, "Kel'thuzad"
    Veklor = 4, "Vek'lor"

    def __init__(self, int_value, *args):
        Enum.__init__(int_value)
        self.title, = args
