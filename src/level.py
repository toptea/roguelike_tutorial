import tcod.map
import numpy as np
import skimage.draw
import random
import const
import entity


# -----------------------------------------------------------------------------
# Room Prefab
# -----------------------------------------------------------------------------

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.rr = None
        self.cc = None

    def center(self):
        cx = int(np.median(self.cc))
        cy = int(np.median(self.rr))
        return cy, cx

    def random_position(self):
        index = random.randint(0, len(self.rr)-1)
        y = self.rr[index]
        x = self.cc[index]
        return y, x

    def intersect(self, other):
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= (other.y2 + 2) and
            self.y2 >= (other.y1 - 2)
        )

    def draw(self, array):
        array[self.rr, self.cc] = True


class Rect(Room):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        self.rr, self.cc = skimage.draw.polygon(
            r=[y, y + h, y + h, y],
            c=[x, x, x + w, x + w]
        )


class Ellipse(Room):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.rr, self.cc = skimage.draw.ellipse(
            r=int(y+h/2),
            c=int(x+w/2),
            r_radius=int(h/2),
            c_radius=int(w/2),
            rotation=random.randint(0, 360)
        )


class Irregular(Room):
    def __init__(self, x, y, w, h, map_width=80, map_height=40, is_rect=True):
        super().__init__(x, y, w, h)
        self.rr, self.cc = self._coordinates(w, h, map_width, map_height, is_rect)

    def _coordinates(self, w, h, map_width, map_height, is_rect):
        while True:

            angle = np.linspace(0, 2 * np.pi, 50)
            r_circle = np.sqrt((w / 2) ** 2 + (h / 2) ** 2)

            # different x, y here
            # represent the circle coordinates
            x = np.round(np.cos(angle) * r_circle, 2)
            y = np.round(np.sin(angle) * r_circle, 2)

            # rectangle coordinates
            if is_rect:
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
            x = self.x1 + x - min(x)  # + 3
            y = self.y1 + y - min(y)  # + 4

            # update width, height
            self.x2 = int(self.x1 + max(x) - min(x))
            self.y2 = int(self.y1 + max(y) - min(y))

            # move room back in bound
            if self.x2 >= map_width - 1:
                diff = int(self.x2 - map_width) + 2
                x -= diff
                self.x1 -= diff
                self.x2 -= diff

            if self.y2 >= map_height - 1:
                diff = int(self.y2 - map_height) + 2
                y -= diff
                self.y1 -= diff
                self.y2 -= diff

            if self.x1 <= 0:
                diff = -self.x1 + 2
                x += diff
                self.x1 += diff
                self.x2 += diff

            if self.y1 <= 0:
                diff = -self.y1 + 2
                y += diff
                self.y1 += diff
                self.y2 += diff

            # there's a bug somewhere... Make sure its definitely in bound
            if self.x1 > 0 or self.x2 > 0 or self.y2 < map_height or self.x2 < map_width:
                return skimage.draw.polygon(y, x)


# -----------------------------------------------------------------------------
# Tunnel Prefab
# -----------------------------------------------------------------------------

def draw_horizontal_tunnel(array, x1, x2, y):
    array[y, min(x1, x2):max(x1, x2) + 1] = True


def draw_vertical_tunnel(array, y1, y2, x):
    array[min(y1, y2):max(y1, y2) + 1, x] = True


def draw_horiz_to_vert_tunnel(array, y1, x1, y2, x2):
    draw_horizontal_tunnel(array, x1, x2, y1)
    draw_vertical_tunnel(array, y1, y2, x2)


def draw_vert_to_horiz_tunnel(array, y1, x1, y2, x2):
    draw_vertical_tunnel(array, y1, y2, x1)
    draw_horizontal_tunnel(array, x1, x2, y2)


def draw_diagonal_tunnel(array, y1, x1, y2, x2):
    x_offset, y_offset = 0, 0
    x_diff = max(x2, x1) - min(x2, x1)
    y_diff = max(y2, y1) - min(y2, y1)
    if x_diff > y_diff:
        x_offset = 1
    else:
        y_offset = 1

    rr1, cc1 = skimage.draw.line(y1, x1, y2, x2)
    rr2, cc2 = skimage.draw.line(y1 + y_offset, x1+x_offset, y2 + y_offset, x2+x_offset)
    array[rr1, cc1] = True
    array[rr2, cc2] = True


# -----------------------------------------------------------------------------
# Game Map
# -----------------------------------------------------------------------------

class GameMap(tcod.map.Map):
    def __init__(self, width, height):
        # self.width = width
        # self.height = height
        # self.transparent = np.zeros((height, width), dtype=np.bool_)
        # self.walkable = np.zeros((height, width), dtype=np.bool_)
        # self.fov = np.zeros((height, width), dtype=np.bool_)
        self.explored = np.zeros((height, width), dtype=np.bool_)
        self.ch = np.zeros((height, width), dtype=np.intc)
        self.fg = np.zeros((height, width), dtype='(3,)u1')
        self.bg = np.zeros((height, width), dtype='(3,)u1')
        super().__init__(width, height)


# -----------------------------------------------------------------------------
# Level Generation
# -----------------------------------------------------------------------------

class Level:
    def __init__(self, **kwargs):
        self.max_rooms = kwargs.get('max_rooms', 12)
        self.room_min_width = kwargs.get('room_min_width', 5)
        self.room_max_width = kwargs.get('room_max_width', 10)
        self.room_min_height = kwargs.get('room_min_height', 5)
        self.room_max_height = kwargs.get('room_max_height', 10)

        self.room_probabilities = (
                kwargs.get('prob_irregular_rect_room', 0.60),
                kwargs.get('prob_irregular_circ_room', 0.35),
                kwargs.get('prob_ellipse_room', 0.05),
                kwargs.get('prob_rect_room', 0.00)
            )

        self.tunnel_probabilities = (
            kwargs.get('prob_h_to_v_tunnel', 0.44),
            kwargs.get('prob_v_to_h_tunnel', 0.44),
            kwargs.get('prob_diagonal_tunnel', 0.12),
        )

        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT
        self.blueprint = np.zeros((const.MAP_HEIGHT + 5, const.MAP_WIDTH + 5), dtype=np.bool_)
        self.blueprint_cropped = self.blueprint[2:-2, 2:-2]
        self.game_map = GameMap(const.MAP_WIDTH, const.MAP_HEIGHT)

        self.rooms = []
        self.entities = []
        self.start_pos = None

    def _gen_room(self):
        """used in _make_blueprint() method"""
        while True:
            w = np.random.randint(self.room_min_width, self.room_max_width)
            h = np.random.randint(self.room_min_height, self.room_max_height)
            x = np.random.randint(1, self.map_width - w - 1)
            y = np.random.randint(1, self.map_height - h - 1)

            room_type = (
                Irregular(x, y, w, h, self.map_width, self.map_height, is_rect=True),
                Irregular(x, y, w-1, h-2, self.map_width, self.map_height, is_rect=False),
                Ellipse(x, y, w, h),
                Rect(x, y, w, h),
            )

            room = np.random.choice(
                a=room_type,
                size=1,
                p=self.room_probabilities
            )[0]

            for r in self.rooms:
                if room.intersect(r):
                    break
            else:
                self.rooms.append(room)
                break

        room.draw(self.blueprint_cropped)

    def _gen_corridor(self):
        """used in _make_blueprint() method"""
        new_y, new_x = self.rooms[-1].center()
        prev_y, prev_x = self.rooms[-2].center()

        draw_tunnel_type = (
            draw_horiz_to_vert_tunnel,
            draw_vert_to_horiz_tunnel,
            draw_diagonal_tunnel,
        )

        draw_tunnel = np.random.choice(
            a=draw_tunnel_type,
            size=1,
            p=self.tunnel_probabilities
        )[0]

        draw_tunnel(self.blueprint_cropped, prev_y, prev_x, new_y, new_x)

    def make_blueprint(self):
        for r in range(self.max_rooms):
            self._gen_room()
            if len(self.rooms) > 1:
                self._gen_corridor()

    def make_map(self):

        # move room in all direction, use the mask as the wall
        # to create the 3d effect, move picture north and south by 2
        floor = self.blueprint[2:-2, 2:-2]
        lnw_roof = floor < self.blueprint[4:, 3:-1]
        lne_roof = floor < self.blueprint[4:, 1:-3]
        lsw_roof = floor < self.blueprint[:-4, 3:-1]
        lse_roof = floor < self.blueprint[:-4, 1:-3]
        ln_roof = floor < self.blueprint[4:, 2:-2]
        ls_roof = floor < self.blueprint[:-4, 2:-2]
        nw_roof = floor < self.blueprint[3:-1, 3:-1]
        ne_roof = floor < self.blueprint[3:-1, 1:-3]
        sw_roof = floor < self.blueprint[1:-3, 3:-1]
        se_roof = floor < self.blueprint[1:-3, 1:-3]
        n_roof = floor < self.blueprint[3:-1, 2:-2]
        s_roof = floor < self.blueprint[1:-3, 2:-2]
        w_roof = floor < self.blueprint[2:-2, 3:-1]
        e_roof = floor < self.blueprint[2:-2, 1:-3]

        roof_wall = (
            ln_roof + lnw_roof + lne_roof +
            ls_roof + lsw_roof + lse_roof +
            n_roof + nw_roof + ne_roof +
            s_roof + sw_roof + se_roof +
            e_roof + w_roof
        )

        # create wall and roof
        char = roof_wall[:-1] << roof_wall[1:]
        char = char.astype(np.int16)

        # remove wall with no roof
        wall_with_no_roof = (char == 1)[1:-1, 1:-1] & (char == 0)[0:-2, 1:-1]
        char[1:-1, 1:-1][wall_with_no_roof] = 249  # blooper

        # change number to tileset
        char[(floor[:-1] == 1)] = 249  # floor
        char[char == 1] = 176  # wall
        char[char == 2] = 219  # roof

        self.game_map.walkable[:] = floor[:-1, 1:]
        self.game_map.walkable[char[:, 1:] == 249] = True  # blooper
        self.game_map.transparent[:] = (
            self.blueprint[2:-3, 3:-2] +
            self.blueprint[3:-2, 3:-2] +
            self.blueprint[1:-4, 3:-2]
        )

        self.game_map.ch[:] = char[:, 1:]
        self.game_map.fg[:] = (220, 220, 220)  # wall, roof, floor,  -> white fg
        # self.game_map.fg[char[:, 1:] == 247] = (0, 120, 255)  # water -> blue fg
        self.game_map.bg[:] = (30, 20, 10)  # wall, roof -> black bg
        self.game_map.bg[floor[:-1, 1:] == True] = (50, 45, 30)  # wall -> grey bg
        self.game_map.bg[char[:, 1:] == 249] = (50, 45, 30)  # blooper -> grey bg

        # see south wall
        fov_fix = (
            (self.game_map.ch == 249)[:-3] &  # floor
            (self.game_map.ch == 219)[1:-2] &  # roof
            (self.game_map.ch == 176)[2:-1] &  # wall
            (self.game_map.ch == 249)[3:]  # foor
        )

        self.game_map.transparent[1:-2] = self.game_map.transparent[1:-2] != fov_fix

        # make diagonal roof not transparent (NW)
        fov_fix2 = (
            self.game_map.transparent[1:-1, 1:-1] &
            (self.game_map.ch == 176)[1:-1, 1:-1] &  # wall
            (self.game_map.ch == 219)[:-2, :-2]  # roof
        )

        # make diagonal roof not transparent (NE)
        fov_fix3 = (
            self.game_map.transparent[1:-1, 1:-1] &
            (self.game_map.ch == 176)[1:-1, 1:-1] &  # wall
            (self.game_map.ch == 219)[:-2, 2:]  # roof
        )

        self.game_map.transparent[:-2, :-2] = self.game_map.transparent[:-2, :-2] > fov_fix2
        self.game_map.transparent[:-2, 2:] = self.game_map.transparent[:-2, 2:] > fov_fix3

    def place_entities(self, create_player=True):
        while True:
            y, x = self.rooms[0].random_position()
            if self.game_map.walkable[y, x]:
                break
        if create_player:
            self.entities.append(entity.player(x, y))
        else:
            self.start_pos = (x, y)

        valid_pos = []
        num_stairs = 1
        for _ in range(num_stairs):
            while True:
                y, x = self.rooms[-1].random_position()
                if self.game_map.walkable[y, x]:
                    valid_pos.append((x, y))
                    break

        for room in range(1, self.max_rooms):
            num_monster = np.random.randint(0, const.MAX_MONSTERS_PER_ROOM)
            num_item = np.random.randint(0, const.MAX_ITEMS_PER_ROOM)
            monster = entity.RandomMonster()
            scroll = entity.RandomScroll()

            for _ in range(num_monster + num_item):
                while True:
                    y, x = self.rooms[room].random_position()
                    if self.game_map.walkable[y, x]:
                        valid_pos.append((x, y))
                        break

            if len(valid_pos) != 0:
                for _ in range(num_monster):
                    x, y = valid_pos.pop()
                    self.entities.append(monster.generate(x, y))

                for _ in range(num_item):
                    x, y = valid_pos.pop()
                    # self.entities.append(entity.healing_potion(x=x, x=y))
                    self.entities.append(scroll.generate(x=x, y=y))
        for _ in range(num_stairs):
            x, y = valid_pos.pop()
            self.entities.append(entity.stairs(x, y))

    def get_start_position(self):
        return self.start_pos
