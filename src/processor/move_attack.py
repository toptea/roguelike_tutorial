import component as c

import esper


class MoveAttack(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):

        # apply velocity to player
        player, (_, pos, vel) = next(self.world.get_components(c.IsPlayer, c.Position, c.Velocity))
        move = self.scene.action.get('move')
        if move:
            vel.dx, vel.dy = move

        # no velocity to player if there's a wall ahead
        if not self.scene.game_map.walkable[(pos.y + vel.dy), (pos.x + vel.dx)]:
            vel.dx, vel.dy = 0, 0
            return None

        # check for collision on other entities
        for other_ent, (_, other_pos) in self.world.get_components(c.Collidable, c.Position):
            if (player != other_ent) and ((pos.x + vel.dx) == other_pos.x) and ((pos.y + vel.dy) == other_pos.y):
                print('collision!')
                vel.dx, vel.dy = 0, 0
                return None

        # set player new x,y position
        pos.x += vel.dx
        pos.y += vel.dy
        vel.dx, vel.dy = 0, 0
        self.scene.fov_compute = True

