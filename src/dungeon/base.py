import numpy as np
import const
import tcod


class GameMap(tcod.map.Map):
    def __init__(self, width, height):
        # self.width = width
        # self.height = height
        # self.transparent = np.zeros((height, width), dtype=np.bool_)
        # self.walkable = np.zeros((height, width), dtype=np.bool_)
        # self.fov = np.zeros((height, width), dtype=np.bool_)
        self.explored = np.zeros((height, width), dtype=np.bool_)
        self.ch = np.zeros((height, width), dtype=np.intc)
        self.fg = np.zeros((height, width), dtype='(3,)u1')
        self.bg = np.zeros((height, width), dtype='(3,)u1')
        super().__init__(width, height)


class Level:
    def __init__(self):
        self.game_map = GameMap(width=const.MAP_WIDTH, height=const.MAP_HEIGHT)
        self.entities = []

    def make_map(self):
        raise NotImplementedError

    def place_entities(self):
        raise NotImplementedError

    def add_to_world(self, world):
        world.create_entity(self.game_map)
        for e in self.entities:
            if len(e) <= 1:
                world.create_entity(e)
            else:
                world.create_entity(*e)
