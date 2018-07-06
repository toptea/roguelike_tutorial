import processor as p
import level
import event
import esper
import tcod
import const


PROCESSOR_GROUP = {
    'player_turn': [
        p.FOV(),
        # p.PlayerAction(),
        p.Render(),
        # p.Collision(),
        # p.UnderStatus(),
        p.MoveAttack(),
        # p.PickUp(),
        # p.Enter(),
        # p.Death(),
        # p.MessageLog(),
        p.Console()
    ],
    'enemy_turn': [
        # p.EnemyAction(),
        p.Render(),
        # p.Collision(),
        # p.UnderStatus(),
        p.MoveAttack(),
        # p.Death(),
        # p.MessageLog(),
    ],
    'show_inventory': [
        # p.InventoryAction(),
        # p.UseHealthItem(),
        # p.UseStatsItem(),
        # p.UseStatusItem(),
        # p.Equip(),

    ],
    'drop_inventory': [
        # p.InventoryAction(),
        # p.Drop(),
    ],
    'target': [
        # p.TargetAction(),
        # p.Targeting(),
    ],
}


class SceneManager:

    def __init__(self, state='game'):
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
            'option': None,
            'game': Game(),
        }
        self.current_scene = self.scenes[state]
        Scene.manager = self

    def change_scene(self, state):
        self.current_scene = self.scenes[state]

    def randomize_scene(self):
        self.current_scene = Game()

    def run(self):
        while not tcod.console_is_window_closed():
            self.current_scene.update()


class Scene:
    manager = None

    def update(self):
        raise NotImplementedError


class Game(Scene):

    def __init__(self):
        self.world = esper.World()
        self.event = event.EventProcessor()
        self.processor_group = PROCESSOR_GROUP
        self.fov_recompute = True
        self.game_map = None

        self.change_processors('player_turn')
        self._create_level()

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
        self.event.process()
        self.world.process()


if __name__ == '__main__':
    app = SceneManager(state='game')
    app.run()
