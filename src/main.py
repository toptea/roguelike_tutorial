import processor
import level
import const

import collections
import esper
import tcod
import pickle


class SceneManager:

    def __init__(self, state='menu'):
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
            'menu': MainMenu(),
            'option': Option(),
            'game': Game(),
        }
        self.current_scene = self.scenes[state]
        Scene.manager = self

    def change_scene(self, state):
        self.current_scene = self.scenes[state]

    def randomize_scene(self):
        self.current_scene = Game()

    def save_game(self):
        with open('data/save/components.pickle', 'wb') as file:
            pickle.dump(
                obj=self.scenes['game'].world._components,
                file=file,
                protocol=pickle.HIGHEST_PROTOCOL
            )

        with open('data/save/entities.pickle', 'wb') as file:
            pickle.dump(
                obj=self.scenes['game'].world._entities,
                file=file,
                protocol=pickle.HIGHEST_PROTOCOL
            )

        with open('data/save/game_map.pickle', 'wb') as file:
            pickle.dump(
                obj=self.scenes['game'].game_map,
                file=file,
                protocol=pickle.HIGHEST_PROTOCOL
            )

        # np.save('game_map', self.scenes['game'].game_map)

    def load_game(self):
        with open('data/save/components.pickle', 'rb') as file:
            components = pickle.load(file)

        with open('data/save/entities.pickle', 'rb') as file:
            entities = pickle.load(file)

        with open('data/save/game_map.pickle', 'rb') as file:
            game_map = pickle.load(file)

        world = esper.World()
        world._components = components
        world._entities = entities
        self.scenes['game'] = Game(world, game_map)
        self.current_scene = self.scenes['game']

    def run(self):
        while not tcod.console_is_window_closed():
            self.current_scene.update()


class Scene:
    manager = None

    def update(self):
        raise NotImplementedError


class Game(Scene):
    def __init__(self, world=esper.World(), game_map=None):
        self.world = world
        self.game_map = game_map
        if game_map is None:
            self._create_level()

        self.astar = tcod.path.AStar(self.game_map.walkable)

        self.processor_group = processor.PROCESSOR_GROUP
        self.change_processors('player_turn')

        self.fov_recompute = True
        self.message = collections.deque()
        self.action = {}
        self.mouse = tcod.Mouse()

        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT
        self.con = tcod.console.Console(
            width=self.map_width,
            height=self.map_height
        )

        self.panel = tcod.console.Console(
            width=const.SCREEN_WIDTH,
            height=const.PANEL_HEIGHT
        )

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
        self.world._processors = self.processor_group[state]
        for processor_instance in self.processor_group[state]:
            processor_instance.world = self.world
            processor_instance.scene = self

    def update(self):
        self.world.process()


class MainMenu(Scene):
    def __init__(self):
        self.world = esper.World()
        self._add_processors()
        self.action = {}

    def _add_processors(self):
        processors = (
            processor.RenderTitle(),
            processor.InputTitle(),
            processor.Console(),
            processor.StateTitle()
        )
        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)
            proc.scene = self

    def update(self):
        self.world.process()


class Option(Scene):
    def update(self):
        raise NotImplementedError


if __name__ == '__main__':
    app = SceneManager(state='menu')
    app.run()
