import component as c
import const

import esper
import tcod

# -----------------------------------------------------------------------------
# TODO - YOLO! Seriously through, I should refactor this using tcod api
# -----------------------------------------------------------------------------


class RenderShowInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        inventory_menu(
            scene=self.scene,
            header='Press the key next to an item to use it, or Esc to cancel.\n',
            inventory=list(self.player_inventory()),
            inventory_width=50,
            screen_width=const.SCREEN_WIDTH,
            screen_height=const.SCREEN_HEIGHT
        )

    def player_inventory(self):
        for _, (_, inventory) in self.world.get_components(c.IsPlayer, c.Inventory):
            for item, (_, desc) in self.world.get_components(c.Carryable, c.Describable):
                if item in inventory.items:
                    yield (item, desc.name)


class RenderDropInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        inventory_menu(
            scene=self.scene,
            header='Press the key next to an item to drop it, or Esc to cancel.\n',
            inventory=list(self.player_inventory()),
            inventory_width=50,
            screen_width=const.SCREEN_WIDTH,
            screen_height=const.SCREEN_HEIGHT
        )

    def player_inventory(self):
        for _, (_, inventory) in self.world.get_components(c.IsPlayer, c.Inventory):
            for item, (_, desc) in self.world.get_components(c.Carryable, c.Describable):
                if item in inventory.items:
                    yield (item, desc.name)


def menu(scene, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(scene.con, 0, 0, width, screen_height, header)
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
    # tcod.console_flush()


def inventory_menu(scene, header, inventory, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item[1] for item in inventory]
    menu(scene, header, options, inventory_width, screen_width, screen_height)


def main_menu(scene, background_image, screen_width, screen_height):
    tcod.image_blit_2x(background_image, 0, 0, 0)

    tcod.console_set_default_foreground(0, tcod.light_yellow)
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, tcod.BKGND_NONE, tcod.CENTER,
                             'TOMBS OF THE ANCIENT KINGS')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), tcod.BKGND_NONE, tcod.CENTER,
                             'By (Your name here)')

    menu(scene, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)
