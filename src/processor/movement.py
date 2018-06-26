import component as c

import esper


class Movement(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, event, game_map, *args):
        for _, (_, pos) in self.world.get_components(c.IsPlayer, c.Position):
            move = event.action.get('move')
            if move:
                dx, dy = move
                destination_x = pos.x + dx
                destination_y = pos.y + dy
                if game_map.walkable[destination_y, destination_x]:
                    pos.x += dx
                    pos.y += dy

                    event.fov_compute = True
