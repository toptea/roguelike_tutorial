import entity
import const
import dungeon.base
import random
import string
import tcod


class MainLevel(dungeon.base.Level):
    def __init__(self, max_rooms=15, room_min_size=6, room_max_size=10):
        super().__init__()
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT
        self.rooms = []

    def _gen_room(self):
        while True:
            w = random.randint(self.room_min_size, self.room_max_size)
            h = random.randint(self.room_min_size, self.room_max_size)
            x = random.randint(1, self.map_width - w - 1)
            y = random.randint(1, self.map_height - h - 1)
            room = Rect(x, y, w, h)

            for other_room in self.rooms:
                if room.intersect(other_room):
                    break
            else:
                self.rooms.append(room)
                break
        create_room(self.game_map, room)

    def _gen_corridor(self):
        new_x, new_y = self.rooms[-1].center()
        prev_x, prev_y = self.rooms[-2].center()
        if random.random() > 0.5:
            create_h_tunnel(self.game_map, prev_x, new_x, prev_y)
            create_v_tunnel(self.game_map, prev_y, new_y, new_x)
        else:
            create_v_tunnel(self.game_map, prev_y, new_y, prev_x)
            create_h_tunnel(self.game_map, prev_x, new_x, new_y)

    def make_map(self):
        for r in range(self.max_rooms):
            self._gen_room()
            if len(self.rooms) > 1:
                self._gen_corridor()

    def place_entities(self):
        x, y = self.rooms[0].center()
        self.entities.append(entity.player(x, y))
        for i in range(1, self.max_rooms):
            x, y = self.rooms[i].center()
            self.entities.append(entity.monster('M', tcod.red, x, y))


class TwoRoomTest(dungeon.base.Level):

    def make_map(self):
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        create_room(self.game_map, room1)
        create_room(self.game_map, room2)
        create_h_tunnel(self.game_map, 25, 40, 23)

    def place_entities(self):
        for _ in range(10):
            self.entities.append(
                entity.monster(
                    char=random.choice(string.ascii_letters),
                    fg=random.choice(const.MONSTER_COLORS),
                    x=random.randint(21, 29),
                    y=random.randint(16, 29),
                )
            )

        self.entities.append(entity.player(x=40, y=20))


class PillarRoomTest(dungeon.base.Level):

    def make_map(self):
        self.game_map.transparent[:] = True
        self.game_map.transparent[::3, 2::3] = False
        self.game_map.transparent[:, 0::const.MAP_WIDTH - 1] = False
        self.game_map.transparent[0::const.MAP_HEIGHT - 1, :] = False
        self.game_map.walkable[:] = self.game_map.transparent[:]

    def place_entities(self):
        self.entities.append(
            entity.player(x=10, y=20)
        )
        self.entities.append(
            entity.monster(char='M', fg=tcod.red, x=20, y=20)
        )


class PillarRoomTest(dungeon.base.Level):

    def make_map(self):
        self.game_map.transparent[:] = True
        self.game_map.transparent[::3, 2::3] = False
        self.game_map.transparent[:, 0::const.MAP_WIDTH - 1] = False
        self.game_map.transparent[0::const.MAP_HEIGHT - 1, :] = False
        self.game_map.walkable[:] = self.game_map.transparent[:]

    def place_entities(self):
        self.entities.append(
            entity.player(x=10, y=20)
        )
        self.entities.append(
            entity.monster(char='M', fg=tcod.red, x=20, y=20)
        )

# -----------------------------------------------------------------------------
# Work in Progress. Generate irregular room with 3d walls.
# -----------------------------------------------------------------------------

import numpy as np
import skimage.draw


def rect(game_map, r0, c0, width, height):
    rr = [r0, r0 + width, r0 + width, r0]
    cc = [c0, c0, c0 + height, c0 + height]
    rr, cc = skimage.draw.polygon(rr, cc)
    game_map.transparent[rr, cc] = True


def irregular_shape(w=20, h=20):
    angle = np.linspace(0, 2 * np.pi, 100)

    # circle coordinates
    r_circle = np.sqrt((w / 2) ** 2 + (h / 2) ** 2)
    x = np.round(np.cos(angle) * r_circle, 2)
    y = np.round(np.sin(angle) * r_circle, 2)

    # rectangle coordinates
    x[x > w / 2] = w / 2
    x[x < -w / 2] = -w / 2
    y[y > h / 2] = h / 2
    y[y < -h / 2] = -h / 2

    # noise for x coordinate
    noise1 = tcod.noise.Noise(
        dimensions=1,
        algorithm=tcod.NOISE_SIMPLEX,
        implementation=tcod.noise.FBM,
        hurst=0.5,
        lacunarity=2,
        octaves=4,
    )

    # noise for y coordinate
    noise2 = tcod.noise.Noise(
        dimensions=1,
        algorithm=tcod.NOISE_SIMPLEX,
        implementation=tcod.noise.FBM,
        hurst=0.5,
        lacunarity=2,
        octaves=4,
    )

    # Return the sampled noise from the grid of points.
    xn = noise1.sample_ogrid([angle])
    yn = noise2.sample_ogrid([angle])

    # start and end return to zero
    xn[:20] = xn[:20] * np.arange(0, 1, 0.05)
    xn[-20:] = xn[-20:] * np.arange(1, 0, -0.05)
    yn[:20] = yn[:20] * np.arange(0, 1, 0.05)
    yn[-20:] = yn[-20:] * np.arange(1, 0, -0.05)

    # add noise
    x = x + x * xn
    y = y + y * yn

    # move origin point
    x = x - min(x) + 3
    y = y - min(y) + 4

    # update width, height
    w = int(max(x) + 5)
    h = int(max(y) + 7)

    # draw to numpy array
    img = np.zeros((h, w), dtype=np.int)
    rr, cc = skimage.draw.polygon(y, x)
    img[rr, cc] = True
    return img


def apply_tileset(img):
    # move picture in all direction, use the mask as the wall
    floor = img[2:-2, 2:-2]
    nw_roof = floor < img[3:-1, 3:-1]
    ne_roof = floor < img[3:-1, 1:-3]
    sw_roof = floor < img[1:-3, 3:-1]
    se_roof = floor < img[1:-3, 1:-3]
    n_roof = floor < img[3:-1, 2:-2]
    s_roof = floor < img[1:-3, 2:-2]
    w_roof = floor < img[2:-2, 3:-1]
    e_roof = floor < img[2:-2, 1:-3]

    roof_wall1 = (
        nw_roof + ne_roof + sw_roof + se_roof +
        n_roof + e_roof + s_roof + w_roof
    )

    # to create the 3d effect, move picture north and south by 2
    floor = img[2:-2, 2:-2]
    lnw_roof = floor < img[4:, 3:-1]
    lne_roof = floor < img[4:, 1:-3]
    lsw_roof = floor < img[:-4, 3:-1]
    lse_roof = floor < img[:-4, 1:-3]
    ln_roof = floor < img[4:, 2:-2]
    ls_roof = floor < img[:-4, 2:-2]
    w_roof = floor < img[2:-2, 3:-1]
    e_roof = floor < img[2:-2, 1:-3]

    roof_wall2 = (
        lnw_roof + lne_roof + lsw_roof + lse_roof +
        ln_roof + ls_roof + roof_wall1
    )

    # create wall and roof
    final = roof_wall2[:-1] << roof_wall2[1:]
    final = final.astype(np.int16)
    # remove wall with no roof
    wall_with_no_roof = (final == 1)[1:-1, 1:-1] & (final == 0)[0:-2, 1:-1]
    final[1:-1, 1:-1][wall_with_no_roof] = 249  # change to floor

    # final[floor] = 3
    final[floor[:-1] == 1] = 249  # floor
    final[final == 1] = 176  # wall
    final[final == 2] = 219  # roof
    return final


class IrregularRoomTest(dungeon.base.Level):

    def make_map(self):
        # top_left
        img = irregular_shape(10, 10)
        img = apply_tileset(img)
        self.game_map.ch[:img.shape[0], :img.shape[1]] = img

        # bottom_left
        img = irregular_shape(10, 10)
        img = apply_tileset(img)
        self.game_map.ch[:img.shape[0], const.MAP_WIDTH - img.shape[1]:] = img

        # top_right
        img = irregular_shape(10, 10)
        img = apply_tileset(img)
        self.game_map.ch[const.MAP_HEIGHT - img.shape[0]:, :img.shape[1]] = img

        # bottom_right
        img = irregular_shape(10, 10)
        img = apply_tileset(img)
        self.game_map.ch[const.MAP_HEIGHT - img.shape[0]:, const.MAP_WIDTH - img.shape[1]:] = img

        self.game_map.walkable[:] = True
        self.game_map.fg[:] = (150, 150, 150)
        self.game_map.bg[:] = (20, 20, 20)


    def place_entities(self):
        self.entities.append(
            entity.player(x=40, y=20)
        )

# -----------------------------------------------------------------------------


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other_rect):
        """returns true if this rectangle intersects with another one"""
        return (
            self.x1 <= other_rect.x2 and
            self.x2 >= other_rect.x1 and
            self.y1 <= other_rect.y2 and
            self.y2 >= other_rect.y1
        )


def create_room(game_map, rect):
    game_map.walkable[rect.y1+1:rect.y2, rect.x1+1:rect.x2] = True
    game_map.transparent[:] = game_map.walkable[:]
    light_ground = game_map.walkable
    game_map.ch[light_ground] = ord('.')
    game_map.fg[light_ground] = (150, 150, 150)
    game_map.bg[light_ground] = (20, 20, 20)

    light_wall = ~game_map.walkable
    game_map.ch[light_wall] = ord('#')
    game_map.fg[light_wall] = (150, 150, 150)
    game_map.bg[light_wall] = (180, 180, 180)


def create_h_tunnel(game_map, x1, x2, y):
    game_map.walkable[y, min(x1, x2):max(x1, x2) + 1] = True
    game_map.transparent[:] = game_map.walkable[:]


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[min(y1, y2):max(y1, y2) + 1, x] = True
        game_map.transparent[:] = game_map.walkable[:]
