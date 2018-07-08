from dataclasses import dataclass
# from util import autoslots
import enum
import tcod


@dataclass
class RenderOrderItem:
    pass


@dataclass
class RenderOrderCorpse:
    pass


@dataclass
class RenderOrderActor:
    pass


@dataclass
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Velocity:
    dx: int = 0
    dy: int = 0


@dataclass
class Collidable:
    pass


@dataclass
class Describable:
    name: str = ''
    desc: str = ''


@dataclass
class IsPlayer:
    pass


@dataclass
class IsHostile:
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
    max_hp: int = hp
    defense: int = 2
    power: int = 5


@dataclass
class Status:
    confuse: bool = False
    paralyse: bool = False
    sleep: bool = False
    poison: bool = False


@dataclass
class HealthModifier:
    delta_hp: int


@dataclass
class HealthModifier:
    delta_hp: int


@dataclass
class StatsModifier:
    delta_defense: int
    delta_power: int


@dataclass
class StatusModifier:
    confuse: bool = False
    paralyse: bool = False
    sleep: bool = False
    poison: bool = False
