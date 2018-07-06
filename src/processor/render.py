import component as c
import const

import esper
import tcod


class Render(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT

        self.con = tcod.console.Console(
            width=self.map_width,
            height=self.map_height
        )

    def process(self, *args):
        game_map = self.scene.game_map
        self.render_map(game_map)
        self.render_all(game_map)
        self.render_fps_counter()
        self.blit_console()
        self.flush_console()
        self.clear_all()

    def render_map(self, game_map):
        if self.scene.event.action.get('reveal_all'):
            self.scene.game_map.explored[:] = True

        # game_map.fov[:] = True
        # self.scene.fov_recompute = True
        if self.scene.fov_recompute:

            light_ground = (game_map.ch==249) & game_map.fov
            self.con.ch[light_ground] = game_map.ch[light_ground]
            self.con.fg[light_ground] = game_map.fg[light_ground]
            self.con.bg[light_ground] = game_map.bg[light_ground]

            light_wall = (game_map.ch==176) & game_map.fov
            self.con.ch[light_wall] = game_map.ch[light_wall]
            self.con.fg[light_wall] = game_map.fg[light_wall]
            self.con.bg[light_wall] = game_map.bg[light_wall]

            light_roof = (game_map.ch == 219) & game_map.fov
            self.con.ch[light_roof] = game_map.ch[light_roof]
            self.con.fg[light_roof] = game_map.fg[light_roof]
            self.con.bg[light_roof] = game_map.bg[light_roof]

            dark_ground = (game_map.ch==249) & ~game_map.fov & game_map.explored
            self.con.ch[dark_ground] = 249
            self.con.fg[dark_ground] = (45, 40, 35)
            self.con.bg[dark_ground] = (30, 20, 10)

            dark_wall = (game_map.ch==176) & ~game_map.fov & game_map.explored
            self.con.ch[dark_wall] = 176
            self.con.fg[dark_wall] = (60, 55, 50)
            self.con.bg[dark_wall] = (30, 20, 10)

            dark_roof = (game_map.ch == 219) & ~game_map.fov & game_map.explored
            self.con.ch[dark_roof] = 219
            self.con.fg[dark_roof] = (60, 55, 50)
            self.con.bg[dark_roof] = (30, 20, 10)

            self.con.ch[~game_map.explored] = 219
            self.con.fg[~game_map.explored] = (15, 10, 5)
            self.con.bg[~game_map.explored] = (15, 10, 5)

    def render_all(self, game_map):
        generator = self.world.get_components(c.Renderable, c.Position)
        for _, (rend, pos) in generator:
            if game_map.fov[pos.y, pos.x]:
                self.con.default_fg = rend.fg
                self.con.default_bg = rend.bg
                self.con.print_(
                    x=pos.x,
                    y=pos.y,
                    string=rend.char,
                    bg_blend=rend.bg_blend
                )

    def render_fps_counter(self):
        self.scene.manager.root_console.default_fg = tcod.grey
        self.scene.manager.root_console.print_(
            x=79, y=46,
            string=' last frame : %3d ms (%3d fps)' % (
                tcod.sys_get_last_frame_length() * 1000.0,
                tcod.sys_get_fps()),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.RIGHT
        )
        self.scene.manager.root_console.print_(
            x=79, y=47,
            string='elapsed : %8d ms %4.2fs' % (
                tcod.sys_elapsed_milli(),
                tcod.sys_elapsed_seconds()),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.RIGHT,
        )

    def blit_console(self):
        self.con.blit(
            dest=self.scene.manager.root_console,
            width=self.map_width,
            height=self.map_height
        )

    def flush_console(self):
        tcod.console_flush()

    def clear_all(self):
        generator = self.world.get_components(c.Renderable, c.Position)
        for _, (rend, pos) in generator:
            self.con.print_(
                x=pos.x,
                y=pos.y,
                string=' ',
                bg_blend=rend.bg_blend
            )
