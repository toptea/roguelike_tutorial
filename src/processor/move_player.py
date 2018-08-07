import component as c
import esper
import tcod


class MovePlayer(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action.get('move'):
            player_c = self.world.get_components(
                c.PlayerTurn,
                c.Movable,
                c.Position,
                c.Describable,
                c.Stats
            )
            for player, (_, _, player_pos, player_desc, player_stats) in player_c:
                new_x = player_pos.x + self.scene.action.get('move')[0]
                new_y = player_pos.y + self.scene.action.get('move')[1]

                # check for collision on map
                if not self.scene.game_map.walkable[new_y, new_x]:
                    break

                # check for collision on other entities
                if self.collide_on_entity(player, new_x, new_y,
                                          player_desc, player_stats):
                    break

                self.scene.fov_compute = True
                player_pos.x = new_x
                player_pos.y = new_y

    def collide_on_entity(self, entity, new_x, new_y, desc, stats):
        collidable_c = self.world.get_components(
            c.Collidable,
            c.Position,
            c.Describable,
            c.Stats
        )
        is_collided = False
        for other_entity, (_, other_pos, other_desc, other_stats) in collidable_c:
            b1 = entity != other_entity
            b2 = new_x == other_pos.x
            b3 = new_y == other_pos.y
            if b1 and b2 and b3:
                is_collided = True
                damage = stats.power - other_stats.defense

                if damage > 0:
                    other_stats.hp -= damage
                    self.scene.message.append(
                        (
                            '{0} attacks {1} for {2} hit points.'.format(
                                desc.name.capitalize(),
                                other_desc.name,
                                str(damage),
                            ),
                            tcod.white
                        )
                    )
                else:
                    self.scene.message.append(
                        (
                            '{0} attacks {1} but does no damage.'.format(
                                desc.name.capitalize(),
                                other_desc.name
                            ),
                            tcod.white
                        )
                    )
        return is_collided
