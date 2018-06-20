import component as c

import esper
import tcod
import sys


class ConsoleProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, event in self.world.get_component(c.Event):
            if event.action.get('exit'):
                sys.exit()

            if event.action.get('fullscreen'):
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
