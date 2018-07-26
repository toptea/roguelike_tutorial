import component as c

import random
import esper
import math
import tcod


class MoveEnemy(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action != {}:
            self.move_enemies()

    def move_enemies(self):
        g_player = self.world.get_components(
            c.PlayerTurn,
            c.Movable,
            c.Position,
            c.Describable,
            c.Stats
        )

        g_enemy = self.world.get_components(
            c.EnemyTurn,
            c.Movable,
            c.Position,
            c.Describable,
            c.Stats,
            c.Status
        )

        for player, (_, _, player_pos, player_desc, player_stats) in g_player:
            for enemy, (_, _, enemy_pos, enemy_desc, enemy_stats, enemy_status) in g_enemy:

                # if enemy is within range, move towards the player
                if self.find_distance(player_pos, enemy_pos) <= 5:
                    new_y, new_x = self.move_toward(enemy_pos, player_pos)

                    #under status
                    if enemy_status.paralyse or enemy_status.freeze:
                        new_x, new_y = enemy_pos.x, enemy_pos.y

                    if enemy_status.confuse:
                        new_x = enemy_pos.x + random.randint(-1, 1)
                        new_y = enemy_pos.y + random.randint(-1, 1)

                        if not self.scene.game_map.walkable[new_y, new_x]:
                            break

                    # check for collision on player
                    if new_x == player_pos.x and new_y == player_pos.y:
                        damage = enemy_stats.power - player_stats.defense

                        if damage > 0:
                            player_stats.hp -= damage
                            self.scene.message.append(
                                (
                                    '{0} attacks {1} for {2} hit points.'.format(
                                        enemy_desc.name.capitalize(),
                                        player_desc.name,
                                        str(damage)
                                    ),
                                    tcod.white
                                )
                            )
                        else:
                            self.scene.message.append(
                                (
                                    '{0} attacks {1} but does no damage.'.format(
                                        enemy_desc.name.capitalize(),
                                        player_desc.name
                                    ),
                                    tcod.white
                                )
                            )
                        return None

                    # check for collision on other entities
                    gen_c = self.world.get_components(c.Collidable, c.Position)
                    for other_ent, (_, other_pos) in gen_c:
                        b1 = enemy != other_ent
                        b2 = new_x == other_pos.x
                        b3 = new_y == other_pos.y
                        if b1 and b2 and b3:
                            self.scene.message.append(('enemy bumped into each other!', tcod.white))
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
