import component as c

import esper


class Movement(esper.Processor):

    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        for _, (_, pos) in self.world.get_components(c.IsPlayer, c.Position):
            move = self.scene.event.action.get('move')
            if move:
                dx, dy = move
                destination_x = pos.x + dx
                destination_y = pos.y + dy
                if self.scene.level.game_map.walkable[destination_y, destination_x]:
                    pos.x += dx
                    pos.y += dy

                    self.scene.fov_compute = True
