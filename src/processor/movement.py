import component as c

import esper


class Movement(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        _, game_map = next(self.world.get_component(c.GameMap))
        for _, (pos, event) in self.world.get_components(c.Position, c.Event):
            move = event.action.get('move')
            if move:
                dx, dy = move
                destination_x = pos.x + dx
                destination_y = pos.y + dy
                if game_map.walkable[destination_y, destination_x]:
                    pos.x += dx
                    pos.y += dy

                    event.fov_compute = True
