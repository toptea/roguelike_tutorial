from dataclasses import dataclass, fields
import const
import tcod


@dataclass
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE
    layer: int = const.LAYER_ACTOR


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Movable:
    pass


@dataclass
class Collidable:
    pass


@dataclass
class Describable:
    name: str = ''
    desc: str = ''


@dataclass
class Inventory:
    items: list
    capacity: int = 2


@dataclass
class PlayerTurn:
    pass


@dataclass
class EnemyTurn:
    pass


@dataclass
class Consumable:
    pass


@dataclass
class Carryable:
    pass


@dataclass
class Wearable:
    pass


@dataclass
class Aimable:
    pass


@dataclass
class Enterable:
    pass


@dataclass
class Stats:
    hp: int = 30
    max_hp: int = 30
    defense: int = 2
    power: int = 5


@dataclass
class Status:
    confuse: bool = False
    paralyse: bool = False
    sleep: bool = False
    poison: bool = False


@dataclass
class StatsModifier:
    hp: int = 0
    max_hp: int = 0
    defense: int = 0
    power: int = 0


@dataclass
class StatusModifier:
    confuse: bool = False
    paralyse: bool = False
    sleep: bool = False
    poison: bool = False


@dataclass
class Experience:
    level: int = 1
    xp: int = 0
    level_up_base: int = 200
    level_up_factor: int = 150

    @property
    def xp_to_next_level(self):
        return (self.level * self.level_up_factor) + self.level_up_base


@dataclass
class ExperienceModifier:
    level: int = 0
    xp: int = 400


# https://github.com/ericvsmith/dataclasses/blob/master/dataclass_tools.py
# def autoslots(cls):
#     if '__slots__' in cls.__dict__:
#         raise TypeError(f'{cls.__name__} already specifies __slots__')
#     cls_dict = dict(cls.__dict__)
#     field_names = tuple(f.name for f in fields(cls))
#     cls_dict['__slots__'] = field_names
#     for field_name in field_names:
#         cls_dict.pop(field_name, None)
#     cls_dict.pop('__dict__', None)
#     qualname = getattr(cls, '__qualname__', None)
#     cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)
#     if qualname is not None:
#         cls.__qualname__ = qualname
#     return cls
