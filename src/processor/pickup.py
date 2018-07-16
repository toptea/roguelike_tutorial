import component as c

import esper
import tcod


class PickUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action.get('pickup'):

            g_player = self.world.get_components(
                c.IsPlayer,
                c.Position,
                c.Inventory
            )

            g_item = self.world.get_components(
                c.Carryable,
                c.Position,
                c.Describable,
            )

            pickup = False
            for _, (_, player_pos, inventory) in g_player:
                for item, (_, item_pos, item_desc) in g_item:

                    if player_pos.x == item_pos.x and player_pos.y == item_pos.y:
                        pickup = True

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

            if not pickup:
                self.scene.message.append(
                    ('There is nothing here to pick up.', tcod.yellow)
                )
