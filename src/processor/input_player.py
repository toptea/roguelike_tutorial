from dataclasses import dataclass
import esper
import tcod


@dataclass
class Key:
    vk: int = 65
    ch: str = chr(0)
    pressed: bool = True
    alt: bool = False
    ctrl: bool = False
    meta: bool = False
    shift: bool = False

    def __key(self):
        return (
            self.vk, self.ch, self.pressed,
            self.alt, self.ctrl, self.meta,
            self.shift
        )

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class InputPlayer(esper.Processor):
    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()
        self.key_code = {
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
            Key(vk=tcod.KEY_F1): {'randomize_scene': True},
            Key(vk=tcod.KEY_F5): {'reveal_all': True},
            Key(vk=tcod.KEY_F12): {'screenshot': True},
            Key(ch='a'): {},
            Key(ch='b'): {'move': (-1, 1)},
            Key(ch='c'): {},
            Key(ch='d'): {'drop_inventory': True},
            Key(ch='e'): {},
            Key(ch='f'): {},
            Key(ch='g'): {'pickup': True},
            Key(ch='h'): {'move': (-1, 0)},
            Key(ch='i'): {'show_inventory': True},
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

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        user_input = Key(
            vk=self.key.vk, ch=chr(self.key.c),
            alt=(self.key.lalt or self.key.ralt),
            ctrl=(self.key.lctrl or self.key.lctrl),
            meta=(self.key.lmeta or self.key.rmeta),
            shift=self.key.shift, pressed=self.key.pressed,
        )

        if tcod.EVENT_KEY_PRESS and user_input in self.key_code:
            self.scene.action = self.key_code[user_input]
        else:
            self.scene.action = {}

        self.scene.mouse = self.mouse
