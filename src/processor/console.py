import esper
import tcod
import sys


class Console(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):

        if self.scene.action.get('exit'):
            sys.exit()

        if self.scene.action.get('save_and_exit'):
            self.scene.manager.save_game()
            sys.exit()

        if self.scene.action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
            self.scene.message.append(('toggle fullscreen', tcod.blue))

        if self.scene.action.get('screenshot'):
            tcod.sys_save_screenshot()
            self.scene.message.append(('save screenshot', tcod.blue))

        if self.scene.action.get('randomize_scene'):
            self.scene.manager.next_level()
