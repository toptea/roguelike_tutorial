import esper
import tcod
import sys


class Console(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):

        if self.scene.action.get('exit'):
            sys.exit()

        if self.scene.action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if self.scene.action.get('screenshot'):
            tcod.sys_save_screenshot()

        if self.scene.action.get('randomize_scene'):
            self.scene.manager.randomize_scene()

