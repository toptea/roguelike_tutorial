import processor
import level
import esper
import tcod
import collections


class Scene:
    manager = None

    def update(self):
        raise NotImplementedError


class Game(Scene):

    def __init__(self):
        self.world = esper.World()
        self.game_map = None
        self._create_level()
        self.astar = tcod.path.AStar(self.game_map.walkable)
        self.processor_group = processor.PROCESSOR_GROUP
        self.state = 'player_turn'
        self.change_processors(self.state)
        self.fov_recompute = True
        self.message = collections.deque()
        self.action = {}

    def _create_level(self):
        lvl = level.Level()
        lvl.make_blueprint()
        lvl.make_map()
        lvl.place_entities()

        for entity in lvl.entities:
            if len(entity) <= 1:
                self.world.create_entity(entity)
            else:
                self.world.create_entity(*entity)
        self.game_map = lvl.game_map

    def change_processors(self, state):
        self.state = state
        self.world._processors = self.processor_group[state]
        for processor_instance in self.processor_group[state]:
            processor_instance.world = self.world
            processor_instance.scene = self

    def update(self):
        self.world.process()


class MainMenu(Scene):
    def update(self):
        raise NotImplementedError


class Option(Scene):
    def update(self):
        raise NotImplementedError
