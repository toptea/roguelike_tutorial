import tcod

TITLE = 'libtcod tutorial revised'

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

FONT_PATH = 'data/consolas10x10.png'
FONT_FLAG = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD

FOV_ALGORITHM = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10


COLORS = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50)
    }

MONSTER_COLORS = (
    tcod.red,
    tcod.flame,
    tcod.orange,
    tcod.amber,
    tcod.yellow,
    tcod.lime,
    tcod.chartreuse,
    tcod.green,
    tcod.sea,
    tcod.turquoise,
    tcod.cyan,
    tcod.sky,
    tcod.azure,
    tcod.blue,
    tcod.han,
    tcod.violet,
    tcod.purple,
    tcod.fuchsia,
    tcod.magenta,
    tcod.pink,
    tcod.crimson,
    tcod.brass,
    tcod.copper,
    tcod.gold,
    tcod.silver,
    tcod.celadon,
    tcod.peach,
    tcod.grey,
    tcod.sepia,
)
