import component as c

import esper


class MoveAttack(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        _, (_, player_pos) = next(self.world.get_components(c.IsPlayer, c.Position))
        move = self.scene.event.action.get('move')
        if move:
            dx, dy = move
            destination_x = player_pos.x + dx
            destination_y = player_pos.y + dy
            if self.scene.game_map.walkable[destination_y, destination_x]:
                player_pos.x += dx
                player_pos.y += dy

                self.scene.fov_compute = True
