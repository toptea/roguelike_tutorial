from dataclasses import dataclass
# from utils import Key
import esper
import tcod
import sys


# -----------------------------------------------------------------------------
# Global Constants
# -----------------------------------------------------------------------------

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = 'libtcod tutorial revised'

MAP_WIDTH = 80
MAP_HEIGHT = 43

FONT_PATH = 'data/consolas10x10.png'
FONT_FLAG = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD


# -----------------------------------------------------------------------------
# Components
# -----------------------------------------------------------------------------

@dataclass
class Event:
    action: dict = None


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE


# -----------------------------------------------------------------------------
# Event Processor
# -----------------------------------------------------------------------------

# Note: didn't get tcod.Key to work in key_code dictionary below.
# End up create my own hashed object instead.

@dataclass
class Key:
    vk: int = 65
    ch: str = chr(0)
    alt: bool = False
    ctrl: bool = False
    meta: bool = False
    shift: bool = False

    def __key(self):
        return self.vk, self.ch, self.alt, self.ctrl, self.shift

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class EventProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.mask = tcod.EVENT_KEY_PRESS # | tcod.EVENT_MOUSE
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        for ent, event in self.world.get_component(Event):
            tcod.sys_check_for_event(self.mask, self.key, self.mouse)
            event.action = self.handle_key()

    def handle_key(self):
        key_code = {
            Key(vk=tcod.KEY_ENTER, ch='\r', alt=True): {'fullscreen': True},
            Key(vk=tcod.KEY_ESCAPE, ch='\x1b'): {'exit': True},
            Key(vk=tcod.KEY_LEFT, shift=True): {'move': (-1, -1)},
            Key(vk=tcod.KEY_RIGHT, shift=True): {'move': (1, -1)},
            Key(vk=tcod.KEY_LEFT, ctrl=True): {'move': (-1, 1)},
            Key(vk=tcod.KEY_RIGHT, ctrl=True): {'move': (1, 1)},
            Key(vk=tcod.KEY_UP): {'move': (0, -1)},
            Key(vk=tcod.KEY_DOWN): {'move': (0, 1)},
            Key(vk=tcod.KEY_LEFT): {'move': (-1, 0)},
            Key(vk=tcod.KEY_RIGHT): {'move': (1, 0)},
            Key(vk=tcod.KEY_KP0): {'move': (0, 0)},
            Key(vk=tcod.KEY_KP1): {'move': (-1, 1)},
            Key(vk=tcod.KEY_KP2): {'move': (0, 1)},
            Key(vk=tcod.KEY_KP3): {'move': (1, 1)},
            Key(vk=tcod.KEY_KP4): {'move': (-1, 0)},
            Key(vk=tcod.KEY_KP5): {'move': (0, 0)},
            Key(vk=tcod.KEY_KP6): {'move': (1, 0)},
            Key(vk=tcod.KEY_KP7): {'move': (-1, -1)},
            Key(vk=tcod.KEY_KP8): {'move': (0, -1)},
            Key(vk=tcod.KEY_KP9): {'move': (1, -1)},
            Key(ch='a'): {},
            Key(ch='b'): {'move': (-1, 1)},
            Key(ch='c'): {},
            Key(ch='d'): {},
            Key(ch='e'): {},
            Key(ch='f'): {},
            Key(ch='g'): {},
            Key(ch='h'): {'move': (-1, 0)},
            Key(ch='i'): {},
            Key(ch='j'): {'move': (0, 1)},
            Key(ch='k'): {'move': (0, -1)},
            Key(ch='l'): {'move': (1, 0)},
            Key(ch='m'): {},
            Key(ch='n'): {'move': (1, 1)},
            Key(ch='o'): {},
            Key(ch='p'): {},
            Key(ch='q'): {},
            Key(ch='r'): {},
            Key(ch='s'): {},
            Key(ch='t'): {},
            Key(ch='u'): {'move': (1, -1)},
            Key(ch='v'): {},
            Key(ch='w'): {},
            Key(ch='x'): {},
            Key(ch='y'): {'move': (-1, -1)},
            Key(ch='z'): {},
            Key(ch='.'): {'move': (0, 0)}
        }

        user_input = Key(
            vk=self.key.vk, ch=chr(self.key.c),
            alt=(self.key.lalt or self.key.ralt),
            ctrl=(self.key.lctrl or self.key.lctrl),
            meta=(self.key.lmeta or self.key.rmeta),
            shift=self.key.shift,
        )
        if user_input in key_code:
            return key_code[user_input]
        return {}


# -----------------------------------------------------------------------------
# Movement Processor
# -----------------------------------------------------------------------------

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (pos, event) in self.world.get_components(Position, Event):
            move = event.action.get('move')
            if move:
                dx, dy = move
                pos.x += dx
                pos.y += dy


# -----------------------------------------------------------------------------
# Render Processor
# -----------------------------------------------------------------------------

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.map_width = MAP_WIDTH
        self.map_height = MAP_HEIGHT

        tcod.console_set_custom_font(
            fontFile=FONT_PATH,
            flags=FONT_FLAG
        )

        self.root_console = tcod.console_init_root(
            w=self.screen_width,
            h=self.screen_height,
            title=TITLE
        )

        self.con = tcod.console.Console(
            width=self.map_width,
            height=self.map_height
        )

    def process(self):

        # render_all
        for ent, (rend, pos) in self.world.get_components(Renderable, Position):
            self.con.default_fg = rend.fg
            self.con.default_bg = rend.bg
            self.con.print_(
                x=pos.x,
                y=pos.y,
                string=rend.char,
                bg_blend=rend.bg_blend
            )

        # blit console
        self.con.blit(
            dest=self.root_console,
            width=self.map_width,
            height=self.map_height
        )

        # flush console
        tcod.console_flush()

        # clear_all
        for ent, (rend, pos) in self.world.get_components(Renderable, Position):
            self.con.print_(
                x=pos.x,
                y=pos.y,
                string=' ',
                bg_blend=rend.bg_blend
            )


# -----------------------------------------------------------------------------
# Console Processor
# -----------------------------------------------------------------------------

class ConsoleProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, event in self.world.get_component(Event):
            if event.action.get('exit'):
                sys.exit()

            if event.action.get('fullscreen'):
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


# -----------------------------------------------------------------------------
# Entity
# -----------------------------------------------------------------------------

def player(x, y):
    return (
        Renderable('@'),
        Position(x, y),
        Event({}),
    )


# -----------------------------------------------------------------------------
# Scene and Game Loop
# -----------------------------------------------------------------------------

class Scene:

    def __init__(self):
        self.world = esper.World()

    def on_start(self):
        """Start adding processors to the world"""
        processors = (
            RenderProcessor(),
            EventProcessor(),
            MovementProcessor(),
            ConsoleProcessor()
        )
        for num, p in enumerate(processors):
            self.world.add_processor(p, priority=num)

    def on_enter(self):
        """Start adding entities to the world"""
        self.world.create_entity(*player(10, 20))

    def on_update(self):
        """Run all processor's process method in the game loop"""
        self.world.process()


def main():
    """game loop"""
    scene = Scene()
    scene.on_start()
    scene.on_enter()
    while not tcod.console_is_window_closed():
        scene.on_update()


if __name__ == '__main__':
    main()
