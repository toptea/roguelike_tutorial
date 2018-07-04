import esper
import tcod
import sys


class Console(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self, *args):

        if self.world.scene.event.action.get('exit'):
            sys.exit()

        if self.world.scene.event.action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if self.world.scene.event.action.get('screenshot'):
            tcod.sys_save_screenshot()

        if self.world.scene.event.action.get('randomize_scene'):
            self.world.scene.director.randomize_scene()
