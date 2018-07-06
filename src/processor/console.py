import esper
import tcod
import sys


class Console(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):

        if self.scene.event.action.get('exit'):
            sys.exit()

        if self.scene.event.action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if self.scene.event.action.get('screenshot'):
            tcod.sys_save_screenshot()

        if self.scene.event.action.get('randomize_scene'):
            self.scene.manager.randomize_scene()
