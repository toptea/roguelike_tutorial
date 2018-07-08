import component as c

import esper
import math


class MoveEnemy(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        self.move_enemies()
        self.scene.change_processors('player_turn')

    def move_enemies(self):
        gen_c = self.world.get_components(
            c.IsPlayer,
            c.Position,
            c.Velocity,
            c.Describable,
            c.Stats
        )
        player, (_, player_pos, player_vel, player_desc, player_stats) = next(gen_c)

        gen_c = self.world.get_components(
            c.IsHostile,
            c.Position,
            c.Velocity,
            c.Describable,
            c.Stats
        )
        for enemy, (_, enemy_pos, enemy_vel, enemy_desc, enemy_stats) in gen_c:

            # if enemy is within range, move towards the player
            if self.find_distance(player_pos, enemy_pos) <= 5:
                new_y, new_x = self.move_toward(enemy_pos, player_pos)

                # check for collision on player
                if new_x == player_pos.x and new_y == player_pos.y:
                    damage = enemy_stats.power - player_stats.defense

                    if damage > 0:
                        player_stats.hp -= damage
                        self.scene.message.append(
                            '{0} attacks {1} for {2} hit points.'.format(
                                enemy_desc.name.capitalize(),
                                player_desc.name,
                                str(damage)
                            )
                        )
                    else:
                        self.scene.message.append(
                            '{0} attacks {1} but does no damage.'.format(
                                enemy_desc.name.capitalize(),
                                player_desc.name
                            )
                        )
                    # self.scene.message.append('{} insults you!'.format(enemy_desc.name))
                    return None

                # check for collision on other entities
                gen_c = self.world.get_components(c.Collidable, c.Position)
                for other_ent, (_, other_pos) in gen_c:
                    b1 = enemy != other_ent
                    b2 = new_x == other_pos.x
                    b3 = new_y == other_pos.y
                    if b1 and b2 and b3:
                        self.scene.message.append('enemy bumped into each other!')
                        return None

                # set enemy new x,y position
                enemy_pos.x = new_x
                enemy_pos.y = new_y

    @staticmethod
    def find_distance(pos, other_pos):
        dx = other_pos.x - pos.x
        dy = other_pos.y - pos.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_toward(self, pos, other_pos):
        path = self.scene.astar.get_path(pos.y, pos.x, other_pos.y, other_pos.x)
        new_y, new_x = path[0]
        return new_y, new_x
