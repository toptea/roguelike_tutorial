import const

import esper
import tcod


class RenderBlitPanel(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):

        self.scene.panel.blit(
            dest=self.scene.manager.root_console,
            dest_x=0,
            dest_y=const.PANEL_Y,
            src_x=0,
            src_y=0,
            width=const.SCREEN_WIDTH,
            height=const.PANEL_HEIGHT,
            fg_alpha=1.0,
            bg_alpha=1.0,
            key_color=None
        )
        self.scene.panel.default_bg = tcod.black
        self.scene.panel.clear()


class RenderBlitConsole(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        self.scene.con.blit(
            dest=self.scene.manager.root_console,
            width=const.MAP_WIDTH,
            height=const.MAP_HEIGHT
        )


class FlushConsole(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        tcod.console_flush()
