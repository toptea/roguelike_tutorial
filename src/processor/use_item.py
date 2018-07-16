import component as c

import esper
import tcod


class UseItem(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action.get('inventory_index'):
            for _, (_, inventory, player_stats) in self.world.get_components(c.IsPlayer, c.Inventory, c.Stats):
                index = int(self.scene.action.get('inventory_index'))
                if index < len(inventory.items):
                    use_item = inventory.items[index]

                    for item, (_, item_stats) in self.world.get_components(c.Carryable, c.StatsModifier):
                        if use_item == item:
                            if player_stats.hp == player_stats.max_hp:
                                self.scene.message.append(
                                    ('You are already at full health', tcod.yellow)
                                )
                            else:
                                player_stats.hp += item_stats.hp
                                if player_stats.hp > player_stats.max_hp:
                                    player_stats.hp = player_stats.max_hp
                                self.scene.message.append(
                                    ('Your wounds start to feel better!', tcod.green)
                                )

                                # player_stats.max_hp += item_stats.max_hp
                                # player_stats.defense += item_stats.defense
                                # player_stats.power += item_stats.power
                                inventory.items.remove(item)
                                self.world.delete_entity(item)
