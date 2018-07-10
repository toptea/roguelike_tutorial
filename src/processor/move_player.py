import component as c

import esper


class MovePlayer(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        move = self.scene.action.get('move')
        if move:
            # apply velocity to player
            gen_c = self.world.get_components(
                c.IsPlayer,
                c.Position,
                c.Movable,
                c.Describable,
                c.Stats
            )
            for player, (_, player_pos, _, player_desc, player_stats) in gen_c:
                player_vel_dx, player_vel_dy = move

                # no velocity to player if there's a wall ahead
                new_x = player_pos.x + player_vel_dx
                new_y = player_pos.y + player_vel_dy
                if not self.scene.game_map.walkable[new_y, new_x]:
                    return None

                # check for collision on other entities
                gen_c = self.world.get_components(
                    c.Collidable,
                    c.Position,
                    c.Describable,
                    c.Stats
                )
                for other_ent, (_, other_pos, other_desc, other_stats) in gen_c:
                    b1 = player != other_ent
                    b2 = new_x == other_pos.x
                    b3 = new_y == other_pos.y
                    if b1 and b2 and b3:
                        damage = player_stats.power - other_stats.defense

                        if damage > 0:
                            other_stats.hp -= damage
                            self.scene.message.append(
                                '{0} attacks {1} for {2} hit points.'.format(
                                    player_desc.name.capitalize(),
                                    other_desc.name,
                                    str(damage)
                                )
                            )
                        else:
                            self.scene.message.append(
                                '{0} attacks {1} but does no damage.'.format(
                                    player_desc.name.capitalize(),
                                    other_desc.name
                                )
                            )
                        return None

                # set player new x,y position
                player_pos.x += player_vel_dx
                player_pos.y += player_vel_dy
                self.scene.fov_compute = True

