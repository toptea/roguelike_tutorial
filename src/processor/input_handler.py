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
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()
        self.key_code = {
            Key(vk=tcod.KEY_ENTER, ch='\r'): {'take_stairs': True},
            Key(vk=tcod.KEY_ENTER, ch='\r', alt=True): {'fullscreen': True},
            Key(vk=tcod.KEY_ESCAPE, ch='\x1b'): {'save_and_exit': True},
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
            Key(vk=tcod.KEY_F1): {'next_level': (None, None)},
            Key(vk=tcod.KEY_F5): {'reveal_all': True},
            Key(vk=tcod.KEY_F12): {'screenshot': True},
            Key(ch='a'): {},
            Key(ch='b'): {'move': (-1, 1)},
            Key(ch='c'): {'show_character_screen': True},
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
            Key(ch='.'): {'move': (0, 0)},
        }

    def process(self):
        # tcod.sys_check_for_event(
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


class InputInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        if tcod.EVENT_KEY_PRESS and self.key.pressed:
            index = self.key.c - ord('a')
            if index >= 0:
                self.scene.action = {'inventory_index': str(index)}
            elif self.key.vk == tcod.KEY_ENTER and self.key.lalt:
                self.scene.action = {'fullscreen': True}
            elif self.key.vk == tcod.KEY_ESCAPE:
                self.scene.action = {'exit': True}
            else:
                self.scene.action = {}


class InputTitle(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        if tcod.EVENT_KEY_PRESS and self.key.pressed:
            if self.key.c == ord('a'):
                self.scene.action = {'new_game': True}
            elif self.key.c == ord('b'):
                self.scene.action = {'load_game': True}
            elif self.key.vk == tcod.KEY_ENTER and self.key.lalt:
                self.scene.action = {'fullscreen': True}
            elif self.key.c == ord('c') or self.key.vk == tcod.KEY_ESCAPE:
                self.scene.action = {'exit': True}
            else:
                self.scene.action = {}


class InputLevelUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        if tcod.EVENT_KEY_PRESS and self.key.pressed:
            if self.key.c == ord('a'):
                self.scene.action = {'level_up': 'hp'}
            elif self.key.c == ord('b'):
                self.scene.action = {'level_up': 'str'}
            elif self.key.c == ord('c'):
                self.scene.action = {'level_up': 'def'}
            elif self.key.vk == tcod.KEY_ENTER and self.key.lalt:
                self.scene.action = {'fullscreen': True}
            else:
                self.scene.action = {}


class InputCharacterScreen(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        if self.key.vk == tcod.KEY_ESCAPE:
            self.scene.action = {'exit': True}
        else:
            self.scene.action = {}


class InputTargeting(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()

    def process(self):
        tcod.sys_wait_for_event(
            mask=tcod.EVENT_ANY,
            k=self.key,
            m=self.mouse,
            flush=False
        )

        x, y = self.mouse.cx, self.mouse.cy
        if self.key.vk == tcod.KEY_ESCAPE:
            self.scene.action = {'exit': True}
        if self.mouse.lbutton_pressed:
            self.scene.action['left_click'] = (x, y)
        if self.mouse.rbutton_pressed:
            self.scene.action['right_click'] = (x, y)
        self.scene.mouse = self.mouse
