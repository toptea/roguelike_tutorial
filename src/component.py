from dataclasses import dataclass
import tcod


@dataclass
class Event:
    action: dict = None


@dataclass
class Position:
    x: int
    y: int

 
@dataclass
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE
