from dataclasses import dataclass
import numpy as np
import tcod.map


@dataclass
class Event:
    action: dict = None
    fov_recompute: bool = True


@dataclass
class IsPlayer:
    pass


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


class GameMap(tcod.map.Map):
    def __init__(self, width, height):
        # self.width = width
        # self.height = height
        # self.transparent = np.zeros((height, width), dtype=np.bool_)
        # self.walkable = np.zeros((height, width), dtype=np.bool_)
        # self.fov = np.zeros((height, width), dtype=np.bool_)
        self.explored = np.zeros((height, width), dtype=np.bool_)
        super().__init__(width, height)
