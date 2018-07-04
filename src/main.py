import processor
import level
import input
import esper
import tcod
import const
import itertools


class Director:

    def __init__(self):
        tcod.console_set_custom_font(
            fontFile=const.FONT_PATH,
            flags=const.FONT_FLAG
        )
        self.root_console = tcod.console_init_root(
            w=const.SCREEN_WIDTH,
            h=const.SCREEN_HEIGHT,
            title=const.TITLE
        )
        self.scenes = {
            'menu': None,
            'game': GameScene(),
        }
        self.current_scene = GameScene()
        GameScene.director = self

    def change_scene(self):
        self.current_scene = self.scenes['game']

    def randomize_scene(self):
        self.current_scene = GameScene()

    def run(self):
        while not tcod.console_is_window_closed():
            self.current_scene.update()


class GameScene:

    director = None

    def __init__(self):
        self.event = input.EventProcessor()

        self.level = level.Level()
        self.level.make_blueprint()
        self.level.make_map()
        self.level.place_entities()

        self.world = GameWorld()
        self.world.create_all_entities(self.level)

        self.fov_recompute = True
        GameWorld.scene = self

    def update(self):
        self.event.process()
        self.world.process()


class GameWorld(esper.World):

    scene = None

    def __init__(self):
        super().__init__()
        self._define_processors()
        self._define_world_reference()
        self._processors = self.processors['player_turn']

    def _define_processors(self):
        self.processors = {
            'player_turn': [
                processor.FOV(),
                processor.Render(),
                processor.Movement(),
                processor.Console()
            ],
            'enemy_turn': [

            ],
            'show_inventory': [

            ],
            'drop_inventory': [

            ],
            'target': [

            ],
        }

    def _define_world_reference(self):
        nested_processors = [p for p in self.processors.values()]
        unique_processors = set(itertools.chain.from_iterable(nested_processors))
        for processor_instance in unique_processors:
            processor_instance.world = self

    def create_all_entities(self, level):
        for entity in level.entities:
            if len(entity) <= 1:
                self.create_entity(entity)
            else:
                self.create_entity(*entity)

    def change_processors(self, state):
        self._processors = self.processors[state]


if __name__ == '__main__':
    game = Director()
    game.run()
