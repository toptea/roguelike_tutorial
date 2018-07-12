import component as c
import const

import esper
import tcod


class RenderUI(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        self.render_player_hp()
        self.render_name_under_mouse()
        # self.render_fps_counter()

    def _render_bar(self, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum * total_width)

        self.scene.panel.default_bg = back_color
        self.scene.panel.rect(
            x=x,
            y=y,
            width=total_width,
            height=1,
            clear=False,
            bg_blend=tcod.BKGND_SCREEN
        )

        self.scene.panel.default_bg = bar_color
        if bar_width > 0:
            self.scene.panel.rect(
                x=x,
                y=y,
                width=bar_width,
                height=1,
                clear=False,
                bg_blend=tcod.BKGND_SCREEN
            )

        self.scene.panel.default_fg = tcod.white
        self.scene.panel.print_(
            x=int(x + total_width / 2),
            y=y,
            string='{0}: {1}/{2}'.format(name, value, maximum),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.CENTER
        )

    def render_player_hp(self):
        for _, (_, stats) in self.world.get_components(c.IsPlayer, c.Stats):
            self._render_bar(
                x=1,
                y=1,
                total_width=const.BAR_WIDTH,
                name='HP',
                value=stats.hp,
                maximum=stats.max_hp,
                bar_color=tcod.light_red,
                back_color=tcod.darker_red
            )

    def render_name_under_mouse(self):
        x = self.scene.mouse.cx
        y = self.scene.mouse.cy
        names = []
        for _, (pos, desc) in self.world.get_components(c.Position, c.Describable):
            if pos.x == x and pos.y == y and self.scene.game_map.fov[pos.y, pos.x]:
                names.append(desc.name)
        names = ', '.join(names)

        self.scene.panel.print_(
            x=1,
            y=0,
            string=names,
        )

    def render_fps_counter(self):
        self.scene.panel.default_fg = tcod.grey
        self.scene.panel.print_(
            x=1, y=3,
            string='last frame : %3d ms (%3d fps)' % (
                tcod.sys_get_last_frame_length() * 1000.0,
                tcod.sys_get_fps()),
            bg_blend=tcod.BKGND_NONE,
            # alignment=tcod.RIGHT
        )
        self.scene.panel.print_(
            x=1, y=4,
            string='elapsed : %8d ms %4.2fs' % (
                tcod.sys_elapsed_milli(),
                tcod.sys_elapsed_seconds()),
            bg_blend=tcod.BKGND_NONE,
            # alignment=tcod.RIGHT,
        )
