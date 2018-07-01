import tcod

TITLE = 'libtcod tutorial revised'

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

FONT_PATH = 'data/font/cp437_12x12.png'
FONT_FLAG = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW

FOV_ALGORITHM = tcod.FOV_SHADOW
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

# default
s1 = {
    'max_rooms': 12,
    'room_min_width': 5,
    'room_max_width': 10,
    'room_min_height': 5,
    'room_max_height': 10,

    'prob_irregular_rect_room': 0.60,
    'prob_irregular_circ_room': 0.40,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.44,
    'prob_v_to_h_tunnel': 0.44,
    'prob_diagonal_tunnel': 0.12
}

# long corridor
s2 = {
    'max_rooms': 20,
    'room_min_width': 3,
    'room_max_width': 5,
    'room_min_height': 3,
    'room_max_height': 4,

    'prob_irregular_rect_room': 0.60,
    'prob_irregular_circ_room': 0.40,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.50,
    'prob_v_to_h_tunnel': 0.50,
    'prob_diagonal_tunnel': 0
}

# monster nest
s3 = {
    'max_rooms': 20,
    'room_min_width': 3,
    'room_max_width': 5,
    'room_min_height': 3,
    'room_max_height': 4,

    'prob_irregular_rect_room': 0.60,
    'prob_irregular_circ_room': 0.40,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.00,
    'prob_v_to_h_tunnel': 0.00,
    'prob_diagonal_tunnel': 1.0
}

# large rooms
s4 = {
    'max_rooms': 5,
    'room_min_width': 10,
    'room_max_width': 12,
    'room_min_height': 10,
    'room_max_height': 12,

    'prob_irregular_rect_room': 0.0,
    'prob_irregular_circ_room': 1.00,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.0,
    'prob_v_to_h_tunnel': 0.0,
    'prob_diagonal_tunnel': 1
}


# monster nest extreme
s5 = {
    'max_rooms': 40,
    'room_min_width': 3,
    'room_max_width': 5,
    'room_min_height': 3,
    'room_max_height': 4,

    'prob_irregular_rect_room': 0.60,
    'prob_irregular_circ_room': 0.40,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.00,
    'prob_v_to_h_tunnel': 0.00,
    'prob_diagonal_tunnel': 1.0
}


# long corridor extreme
s6 = {
    'max_rooms': 40,
    'room_min_width': 3,
    'room_max_width': 5,
    'room_min_height': 3,
    'room_max_height': 4,

    'prob_irregular_rect_room': 0.60,
    'prob_irregular_circ_room': 0.40,
    'prob_ellipse_room': 0.00,
    'prob_rect_room': 0.00,

    'prob_h_to_v_tunnel': 0.50,
    'prob_v_to_h_tunnel': 0.50,
    'prob_diagonal_tunnel': 0
}