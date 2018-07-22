import component as c

import esper
import tcod


class TakeStairs(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player_item(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Position,
            c.Inventory,
            c.Stats
        )
        for player, (_, player_pos, inventory, stats) in iterable:
            yield (player, player_pos, inventory, stats)

    def get_stairs(self):
        iterable = self.world.get_components(c.Enterable, c.Position)
        for _, (_, stairs_pos) in iterable:
            yield stairs_pos

    def get_player_on_stairs(self):
        for player, player_pos, inventory, stats in self.get_player_item():
            for stairs_pos in self.get_stairs():
                if player_pos.x == stairs_pos.x and player_pos.y == stairs_pos.y:
                    yield (player, inventory, stats)

    def process(self, *args):
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
