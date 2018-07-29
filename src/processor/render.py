import component as c
import textwrap
import const

import esper
import tcod


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]


class RenderConsole(esper.Processor):
    scene = None

    def __init__(self, targeting=False):
        super().__init__()
        self.targeting = targeting
        self.width = const.MAP_WIDTH
        self.height = const.MAP_HEIGHT

    def get_entities(self):
        # not optimal, but it works!
        iterable = list(self.world.get_components(c.Renderable, c.Position))
        iterable.sort(key=lambda row: row[1][0].layer)
        for _, (rend, pos) in iterable:
            yield (rend, pos)

    def process(self):
        self.render_map()
        self.render_entity()
        if self.targeting:
            self.render_target_cursor()
        self.blit_console()
        self.flush_console()
        self.clear_entity()

    def render_map(self):
        if self.scene.action.get('reveal_all'):
            self.scene.game_map.explored[:] = True

        if self.scene.fov_recompute:
            game_map = self.scene.game_map
            con = self.scene.con

            light_ground = (game_map.ch == 249) & game_map.fov
            con.ch[light_ground] = game_map.ch[light_ground]
            con.fg[light_ground] = game_map.fg[light_ground]
            con.bg[light_ground] = game_map.bg[light_ground]

            light_wall = (game_map.ch == 176) & game_map.fov
            con.ch[light_wall] = game_map.ch[light_wall]
            con.fg[light_wall] = game_map.fg[light_wall]
            con.bg[light_wall] = game_map.bg[light_wall]

            light_roof = (game_map.ch == 219) & game_map.fov
            con.ch[light_roof] = game_map.ch[light_roof]
            con.fg[light_roof] = game_map.fg[light_roof]
            con.bg[light_roof] = game_map.bg[light_roof]

            dark_ground = (game_map.ch == 249) & ~game_map.fov & game_map.explored
            con.ch[dark_ground] = 249
            con.fg[dark_ground] = (45, 40, 35)
            con.bg[dark_ground] = (30, 20, 10)

            dark_wall = (game_map.ch == 176) & ~game_map.fov & game_map.explored
            con.ch[dark_wall] = 176
            con.fg[dark_wall] = (60, 55, 50)
            con.bg[dark_wall] = (30, 20, 10)

            dark_roof = (game_map.ch == 219) & ~game_map.fov & game_map.explored
            con.ch[dark_roof] = 219
            con.fg[dark_roof] = (60, 55, 50)
            con.bg[dark_roof] = (30, 20, 10)

    def render_entity(self):
        for (rend, pos) in self.get_entities():
            if self.scene.game_map.fov[pos.y, pos.x]:
                self.scene.con.default_fg = rend.fg
                # self.scene.con.default_bg = rend.bg
                self.scene.con.print_(
                    x=pos.x,
                    y=pos.y,
                    string=rend.char,
                    bg_blend=rend.bg_blend
                )

    def render_target_cursor(self):
        if self.scene.game_map.fov[self.scene.mouse.cy, self.scene.mouse.cx]:
            self.scene.con.default_fg = tcod.red
            self.scene.con.print_(
                x=self.scene.mouse.cx,
                y=self.scene.mouse.cy,
                string='X',
                bg_blend=tcod.BKGND_NONE
            )

    def blit_console(self):
        self.scene.con.blit(
            dest=self.scene.manager.root_console,
            width=self.width,
            height=self.height
        )

    def flush_console(self):
        tcod.console_flush()

    def clear_entity(self):
        for (rend, pos) in self.get_entities():
            if self.scene.game_map.fov[pos.y, pos.x]:
                self.scene.con.print_(
                    x=pos.x,
                    y=pos.y,
                    string=' ',
                    bg_blend=rend.bg_blend
                )


class RenderPanel(esper.Processor, metaclass=Singleton):
    scene = None

    def __init__(self):
        super().__init__()
        self.display_message = []
        self.msg_width = const.MESSAGE_WIDTH
        self.msg_height = const.MESSAGE_HEIGHT
        self.msg_x = const.MESSAGE_X

    def get_player_stats(self):
        iterable = self.world.get_components(c.PlayerTurn, c.Stats)
        for _, (_, stats) in iterable:
            yield stats

    def get_position_under_mouse(self):
        x, y = self.scene.mouse.cx, self.scene.mouse.cy
        iterable = self.world.get_components(c.Position, c.Describable)
        for _, (pos, desc) in iterable:
            if pos.x == x and pos.y == y:
                yield (pos, desc)

    def process(self):
        self.render_player_hp()
        self.render_name_under_mouse()
        self.render_message()
        self.blit_panel()
        self._render_fps_counter(self.scene.panel)

    def render_player_hp(self):
        for stats in self.get_player_stats():
            self._render_bar(
                panel=self.scene.panel,
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
        names = []
        for (pos, desc) in self.get_position_under_mouse():
            if self.scene.game_map.fov[pos.y, pos.x]:
                names.append(desc.name)
        names = ', '.join(names)

        self.scene.panel.print_(
            x=1,
            y=0,
            string=names,
        )

    def render_message(self):
        if len(self.scene.message) > 0:
            while self.scene.message:
                message, color = self.scene.message.popleft()
                new_msg_lines = textwrap.wrap(message, self.msg_width)

                for line in new_msg_lines:
                    if len(self.display_message) == self.msg_height:
                        self.display_message.pop(0)
                    self.display_message.append((line, color))

        for y, (message, color) in enumerate(self.display_message):
            self.scene.panel.default_fg = color
            self.scene.panel.print_(
                x=self.msg_x,
                y=y + 1,
                string=message,
                bg_blend=tcod.BKGND_NONE,
                alignment=tcod.LEFT
            )

    def blit_panel(self):
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

    @staticmethod
    def _render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum * total_width)

        panel.default_bg = back_color
        panel.rect(
            x=x,
            y=y,
            width=total_width,
            height=1,
            clear=False,
            bg_blend=tcod.BKGND_SCREEN
        )

        panel.default_bg = bar_color
        if bar_width > 0:
            panel.rect(
                x=x,
                y=y,
                width=bar_width,
                height=1,
                clear=False,
                bg_blend=tcod.BKGND_SCREEN
            )

        panel.default_fg = tcod.white
        panel.print_(
            x=int(x + total_width / 2),
            y=y,
            string='{0}: {1}/{2}'.format(name, value, maximum),
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.CENTER
        )

    @staticmethod
    def _render_fps_counter(console):
        console.default_fg = tcod.grey
        console.print_(
            x=1, y=3,
            string='fps: %3d fps' % (tcod.sys_get_fps()),
            bg_blend=tcod.BKGND_NONE,
        )
        console.print_(
            x=1, y=4,
            string='last frame: %2d ms' % (
                tcod.sys_get_last_frame_length() * 1000.0,
            ),
            bg_blend=tcod.BKGND_NONE,
        )
        console.print_(
            x=1, y=5,
            string='elapsed: %4.2fs' % (tcod.sys_elapsed_seconds()),
            bg_blend=tcod.BKGND_NONE,
        )


class RenderInventory(esper.Processor):
    scene = None

    def __init__(self, header_type):
        super().__init__()
        if header_type == 'show':
            self.header = (
                'Press the key next to an item to use it, or Esc to cancel.\n'
            )
        if header_type == 'drop':
            self.header = (
                'Press the key next to an item to drop it, or Esc to cancel.\n'
            )

    def get_player_inventory(self):
        iterable_1 = self.world.get_components(c.PlayerTurn, c.Inventory)
        iterable_2 = self.world.get_components(c.Carryable, c.Describable)
        for _, (_, inventory) in iterable_1:
            for item, (_, desc) in iterable_2:
                if item in inventory.items:
                    yield (item, desc.name)

    def process(self, *args):
        inventory = list(self.get_player_inventory())
        if len(inventory) == 0:
            options = ['Inventory is empty.']
        else:
            options = [item[1] for item in inventory]

        _menu(
            scene=self.scene,
            header=self.header,
            options=options,
            width=50,
            screen_width=const.SCREEN_WIDTH,
            screen_height=const.SCREEN_HEIGHT
        )

        tcod.console_flush()


class RenderTitle(esper.Processor):
    scene = None

    def __init__(self):
        self.image = tcod.image_load('data/menu_background.png')
        self.title = 'TOMBS OF THE ANCIENT KINGS'
        self.author = 'By toptea'
        super().__init__()

    def process(self):
        self.image.blit_2x(
            self.scene.manager.root_console, 0, 0)

        self.scene.manager.root_console.default_fg = tcod.white
        self.scene.manager.root_console.print_(
            x=(const.SCREEN_WIDTH - len(self.title)) // 2,
            y=const.SCREEN_HEIGHT // 2 - 4,
            string=self.title,
        )

        self.scene.manager.root_console.print_(
            x=(const.SCREEN_WIDTH - len(self.author)) // 2,
            y=const.SCREEN_HEIGHT - 2,
            string=self.author,
        )

        _menu(
            scene=self.scene,
            header='',
            options=['Play a new game', 'Continue last game', 'Quit'],
            width=24,
            screen_width=const.SCREEN_WIDTH,
            screen_height=const.SCREEN_HEIGHT
        )

        tcod.console_flush()


class RenderLevelUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Stats,
        )
        for _, (_, stats) in iterable:
            yield stats

    def process(self):
        for stats in self.get_player():
            options = [
                'Constitution (+20 HP, from {0})'.format(stats.max_hp),
                'Strength (+1 attack, from {0})'.format(stats.power),
                'Agility (+1 defense, from {0})'.format(stats.defense)
            ]

            _menu(
                scene=self.scene,
                header='Level up! Choose a stat to raise:',
                options=options,
                width=40,
                screen_width=const.SCREEN_WIDTH,
                screen_height=const.SCREEN_HEIGHT
            )

            tcod.console_flush()


class RenderCharacterScreen(esper.Processor):
    scene = None

    def __init__(self):
        self.width = 30
        self.height = 10
        super().__init__()

    def get_player_info(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Stats,
            c.Experience,
        )
        info = []
        for _, (_, stats, exp) in iterable:
            info = [
                'Character Information',
                '',
                'Level: {0}'.format(exp.level),
                'Experience: {0}'.format(exp.xp),
                'Experience to Level: {0}'.format(exp.xp_to_next_level),
                'Maximum HP: {0}'.format(stats.max_hp),
                'Attack: {0}'.format(stats.power),
                'Defense: {0}'.format(stats.defense)
            ]
        return info

    def process(self):

        window = tcod.console_new(self.width, self.height)
        tcod.console_set_default_foreground(window, tcod.white)
        """(con, x, y, w, h, flag, alignment, fmt)"""

        info = self.get_player_info()
        for y, text in enumerate(info):
            tcod.console_print_rect_ex(
                con=window,
                x=0, y=y,
                w=self.width,
                h=self.height,
                flag=tcod.BKGND_NONE,
                alignment=tcod.LEFT,
                fmt=text
            )

        x = const.SCREEN_WIDTH // 2 - self.width // 2
        y = const.SCREEN_HEIGHT // 2 - self.height // 2
        window.blit(
            dest=self.scene.manager.root_console,
            dest_x=x,
            dest_y=y,
            src_x=0,
            src_y=0,
            width=self.width,
            height=self.height,
            fg_alpha=1.0,
            bg_alpha=0.7,
            key_color=None
        )
        tcod.console_flush()


def _menu(scene, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(scene.manager.root_console, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)
    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)

    window.blit(
        dest=scene.manager.root_console,
        dest_x=x,
        dest_y=y,
        src_x=0,
        src_y=0,
        width=width,
        height=height,
        fg_alpha=1.0,
        bg_alpha=0.7,
        key_color=None
    )