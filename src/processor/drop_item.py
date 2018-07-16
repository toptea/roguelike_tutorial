import component as c

import esper
import tcod


class DropItem(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action.get('inventory_index'):
            for _, (_, inventory, pos) in self.world.get_components(c.IsPlayer, c.Inventory, c.Position):
                index = int(self.scene.action.get('inventory_index'))
                if index < len(inventory.items):
                    drop_item = inventory.items[index]

                    for item, (_, desc) in self.world.get_components(c.Carryable, c.Describable):
                        if drop_item == item:

                            self.scene.message.append(
                                ('You dropped the {0}'.format(desc.name), tcod.yellow)
                            )
                            self.world.add_component(item, c.Position(x=pos.x, y=pos.y))
                            inventory.items.remove(item)

