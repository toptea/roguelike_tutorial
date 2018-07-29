import processor
import component as c
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
            title=const.TITLE,
            renderer=tcod.RENDERER_GLSL
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

    def next_level(self, player_entity=None, item_entities=None):
        if player_entity:
            world = self.scenes['game'].world
            entities = world._entities.copy()
            for ent in (ent for ent in entities.keys() if ent != player_entity and ent not in item_entities):
                world.delete_entity(ent, immediate=True)

            self.scenes['game'] = Game(world=world, create_player=False)
            player_pos = self.scenes['game'].world.component_for_entity(player_entity, c.Position)
            x, y = self.scenes['game'].start_pos
            player_pos.x = x
            player_pos.y = y
        else:
            self.scenes['game'] = Game()
        self.current_scene = self.scenes['game']

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
    def __init__(self, world=None, game_map=None, create_player=True):
        self.start_pos = None
        self.world = world
        self.game_map = game_map
        if world is None:
            self.world = esper.CachedWorld()
        if game_map is None:
            self._create_level(create_player)
        self.astar = tcod.path.AStar(self.game_map.walkable)

        self.processor_group = processor.PROCESSOR_GROUP
        self.change_processors('player_turn')

        self.fov_recompute = True
        self.message = collections.deque()
        self.action = {}
        self.mouse = tcod.Mouse()

        self.con = tcod.console.Console(
            width=const.MAP_WIDTH,
            height=const.MAP_HEIGHT
        )
        self._render_unexplored_map()

        self.panel = tcod.console.Console(
            width=const.SCREEN_WIDTH,
            height=const.PANEL_HEIGHT
        )

    def _create_level(self, create_player):
        lvl = level.Level()
        lvl.make_blueprint()
        lvl.make_map()
        lvl.place_entities(create_player)

        for entity in lvl.entities:
            if len(entity) <= 1:
                self.world.create_entity(entity)
            else:
                self.world.create_entity(*entity)
        self.start_pos = lvl.get_start_position()
        self.game_map = lvl.game_map

    def _render_unexplored_map(self):
        self.con.ch[:] = 219
        self.con.fg[:] = (15, 10, 5)
        self.con.bg[:] = (15, 10, 5)

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
