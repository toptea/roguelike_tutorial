import component as c

import esper
import tcod


class TakeStairs(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player_on_stairs(self):
        player_components = self.world.get_components(
            c.PlayerTurn,
            c.Position,
            c.Inventory,
            c.Stats
        )

        stairs_components = self.world.get_components(
            c.Enterable,
            c.Position
        )

        for player, (_, player_pos, inventory, stats) in player_components:
            for _, (_, stairs_pos) in stairs_components:
                if player_pos.x == stairs_pos.x and player_pos.y == stairs_pos.y:
                    yield (player, inventory, stats)

    def process(self):
        if self.scene.action.get('take_stairs'):
            for player, inventory, stats in self.get_player_on_stairs():

                stats.hp += stats.max_hp // 2
                if stats.hp > stats.max_hp:
                    stats.hp = stats.max_hp
                self.scene.message.append(
                    ('You take a moment to rest, and recover your strength', tcod.light_violet)
                )
                self.scene.action = {'next_level': (player, inventory.items)}
                break
            else:
                self.scene.message.append(
                    ('There are no stairs here', tcod.yellow)
                )
