import component as c
import const

import esper
import tcod


class Render(esper.Processor):
    def __init__(self):
        super().__init__()

        self.screen_width = const.SCREEN_WIDTH
        self.screen_height = const.SCREEN_HEIGHT
        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT

        tcod.console_set_custom_font(
            fontFile=const.FONT_PATH,
            flags=const.FONT_FLAG
        )

        self.root_console = tcod.console_init_root(
            w=self.screen_width,
            h=self.screen_height,
            title=const.TITLE
        )

        self.con = tcod.console.Console(
            width=self.map_width,
            height=self.map_height
        )

    def process(self, event, game_map, *args):
        self.render_map(game_map, event)
        self.render_all(game_map)
        self.render_fps_counter()
        self.blit_console()
        self.flush_console()
        self.clear_all()

    def render_map(self, game_map, event):
        if event.action.get('reveal_all'):
            game_map.explored[:] = True

        game_map.fov[:] = True
        event.fov_recompute = True
        if event.fov_recompute:

            light_ground = game_map.walkable & game_map.fov
            self.con.ch[light_ground] = game_map.ch[light_ground]
            self.con.fg[light_ground] = game_map.fg[light_ground]
            self.con.bg[light_ground] = game_map.bg[light_ground]

            light_wall = ~game_map.walkable & game_map.fov
            self.con.ch[light_wall] = game_map.ch[light_wall]
            self.con.fg[light_wall] = game_map.fg[light_wall]
            self.con.bg[light_wall] = game_map.bg[light_wall]

            dark_ground = game_map.walkable & ~game_map.fov & game_map.explored
            self.con.ch[dark_ground] = 250
            self.con.fg[dark_ground] = (20, 20, 20)
            self.con.bg[dark_ground] = (0, 0, 0)

            dark_wall = ~game_map.walkable & ~game_map.fov & game_map.explored
            self.con.ch[dark_wall] = ord(' ')
            self.con.fg[dark_wall] = (20, 20, 20)
            self.con.bg[dark_wall] = (20, 20, 20)

            # original libtcod tutorial theme
            # self.con.bg[game_map.walkable & game_map.fov] = const.COLORS.get('light_ground')
            # self.con.bg[~game_map.walkable & game_map.fov] = const.COLORS.get('light_wall')
            # self.con.bg[game_map.walkable & ~game_map.fov & game_map.explored] = const.COLORS.get('dark_ground')
            # self.con.bg[~game_map.walkable & ~game_map.fov & game_map.explored] = const.COLORS.get('dark_wall')

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
        self.root_console.default_fg = tcod.grey
        self.root_console.print_(
            x=79, y=46,
            string=' last frame : %3d ms (%3d fps)' % (
                tcod.sys_get_last_frame_length() * 1000.0,
                tcod.sys_get_fps()),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.RIGHT
        )
        self.root_console.print_(
            x=79, y=47,
            string='elapsed : %8d ms %4.2fs' % (
                tcod.sys_elapsed_milli(),
                tcod.sys_elapsed_seconds()),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.RIGHT,
        )

    def blit_console(self):
        self.con.blit(
            dest=self.root_console,
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
