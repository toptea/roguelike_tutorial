from dataclasses import dataclass, fields
import const
import tcod


def auto_slots(cls):
    # https://github.com/ericvsmith/dataclasses/blob/master/dataclass_tools.py
    if '__slots__' in cls.__dict__:
        raise TypeError(f'{cls.__name__} already specifies __slots__')
    cls_dict = dict(cls.__dict__)
    field_names = tuple(f.name for f in fields(cls))
    cls_dict['__slots__'] = field_names
    for field_name in field_names:
        cls_dict.pop(field_name, None)
    cls_dict.pop('__dict__', None)
    qualname = getattr(cls, '__qualname__', None)
    cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)
    if qualname is not None:
        cls.__qualname__ = qualname
    return cls


def component(cls):
    return auto_slots(dataclass(cls))


@component
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE
    layer: int = const.LAYER_ACTOR


@component
class Position:
    x: int
    y: int


@component
class Movable:
    pass


@component
class Collidable:
    pass


@component
class Describable:
    name: str = ''
    desc: str = ''


@component
class Inventory:
    items: list
    capacity: int = 2


@component
class PlayerTurn:
    pass


@component
class EnemyTurn:
    pass


@component
class Consumable:
    pass


@component
class Carryable:
    pass


@component
class Wearable:
    pass


@component
class Aimable:
    pass


@component
class Enterable:
    pass


@component
class Stats:
    hp: int = 30
    max_hp: int = 30
    defense: int = 2
    power: int = 5


@component
class Status:
    countdown: int = 0
    confuse: bool = False
    paralyse: bool = False
    freeze: bool = False
    burn: bool = False


@component
class StatsModifier:
    hp: int = 0
    max_hp: int = 0
    defense: int = 0
    power: int = 0


@component
class StatusModifier:
    countdown: int = 3
    confuse: bool = False
    paralyse: bool = False
    freeze: bool = False
    burn: bool = False


@component
class Experience:
    level: int = 1
    xp: int = 0
    level_up_base: int = 200
    level_up_factor: int = 150

    @property
    def xp_to_next_level(self):
        return (self.level * self.level_up_factor) + self.level_up_base


@component
class ExperienceModifier:
    level: int = 0
    xp: int = 400
