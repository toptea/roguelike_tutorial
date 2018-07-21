import component as c

import esper
import tcod


class PickUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Position,
            c.Inventory
        )
        for _, (_, player_pos, inventory) in iterable:
            yield (player_pos, inventory)

    def get_items(self):
        iterable = self.world.get_components(
            c.Carryable,
            c.Position,
            c.Describable,
        )
        for item, (_, item_pos, item_desc) in iterable:
            yield (item, item_pos, item_desc)

    def get_pickup_item(self):
        for player_pos, inventory in self.get_player():
            for item, item_pos, item_desc in self.get_items():
                if player_pos.x == item_pos.x and player_pos.y == item_pos.y:
                    yield (item, item_pos, item_desc, player_pos, inventory)

    def process(self, *args):
        if self.scene.action.get('pickup'):
            for item, item_pos, item_desc, player_pos, inventory in self.get_pickup_item():
                if len(inventory.items) >= inventory.capacity:
                    self.scene.message.append(
                        ('You cannot carry any more, your inventory is full.', tcod.yellow)
                    )
                else:
                    self.scene.message.append(
                        ('You pick up the {0}!'.format(item_desc.name), tcod.cyan)
                    )
                    inventory.items.append(item)
                    self.world.remove_component(item, c.Position)
            else:
                self.scene.message.append(
                    ('There is nothing here to pick up.', tcod.yellow)
                )
