import processor
import level
import input
import esper
import tcod
import const


class Director:

    def __init__(self):
        GameScene.director = self

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
            'mean': None,
            'game': GameScene(),
        }
        self.current_scene = GameScene()

    def load_scene(self):
        self.current_scene = GameScene()

    def run(self):
        while not tcod.console_is_window_closed():
            self.current_scene.update()


class GameScene:

    director = None

    def __init__(self):
        self.event = input.EventProcessor()
        self.level = level.Level()
        self.world = esper.World()

        self.fov_recompute = True

        self._load_processors()
        self._load_level()
        self._load_entities()

    def _load_processors(self):
        processors = (
            processor.FOV(),
            processor.Render(),
            processor.Movement(),
            processor.Console()
        )
        for priority, processor_ in enumerate(processors):
            self.world.add_processor(processor_, priority)
            processor_.scene = self

    def _load_level(self):
        self.level.make_blueprint()
        self.level.make_map()
        self.level.place_entities()

    def _load_entities(self):
        for entity in self.level.entities:
            if len(entity) <= 1:
                self.world.create_entity(entity)
            else:
                self.world.create_entity(*entity)

    def update(self):
        self.event.process()
        self.world.process()


if __name__ == '__main__':
    game = Director()
    game.run()
