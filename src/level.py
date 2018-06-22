import entity
import const

import random
import string
import tcod


class Level:
    def __init__(self):
        self.game_map = entity.game_map()
        self.entities = []

    def make_map(self):
        raise NotImplementedError

    def place_entities(self):
        raise NotImplementedError

    def add_to_world(self, world):
        world.create_entity(self.game_map)
        for e in self.entities:
            if len(e) <= 1:
                world.create_entity(e)
            else:
                world.create_entity(*e)


class MainLevel(Level):
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


class TwoRoomTest(Level):

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


class PillarRoomTest(Level):

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


def create_h_tunnel(game_map, x1, x2, y):
    game_map.walkable[y, min(x1, x2):max(x1, x2) + 1] = True
    game_map.transparent[:] = game_map.walkable[:]


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[min(y1, y2):max(y1, y2) + 1, x] = True
        game_map.transparent[:] = game_map.walkable[:]
