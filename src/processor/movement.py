import component as c

import esper


class Movement(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self, *args):
        _, (_, player_pos) = next(self.world.get_components(c.IsPlayer, c.Position))
        move = self.world.scene.event.action.get('move')
        if move:
            dx, dy = move
            destination_x = player_pos.x + dx
            destination_y = player_pos.y + dy
            if self.world.scene.level.game_map.walkable[destination_y, destination_x]:
                player_pos.x += dx
                player_pos.y += dy

                self.world.scene.fov_compute = True
