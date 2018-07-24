import component as c

import esper
import tcod


class UpdateUseInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player_item(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Inventory,
            c.Stats
        )
        for _, (_, inventory, stats) in iterable:
            index = int(self.scene.action.get('inventory_index'))
            if index < len(inventory.items):
                use_item = inventory.items[index]
                yield (use_item, inventory, stats)

    def get_use_comsumable(self):
        iterable = self.world.get_components(
            c.Carryable,
            c.Consumable,
            c.StatsModifier
        )
        for (use_item, inventory, stats) in self.get_player_item():
            for item, (_, _, modifier) in iterable:
                if use_item == item:
                    yield (item, inventory, stats, modifier)

    def process(self, *args):
        if self.scene.action.get('inventory_index'):
            self.use_consumable()
            self.use_aimable()

    def use_consumable(self):
        for item, inventory, stats, modifier in self.get_use_comsumable():
            if stats.hp == stats.max_hp:
                self.scene.message.append(
                    ('You are already at full health', tcod.yellow)
                )
            else:
                stats.hp += modifier.hp
                if stats.hp > stats.max_hp:
                    stats.hp = stats.max_hp
                self.scene.message.append(
                    ('Your wounds start to feel better!', tcod.green)
                )
                inventory.items.remove(item)
                self.world.delete_entity(item)

    def use_aimable(self):
        scroll_components = self.world.get_components(
            c.Carryable,
            c.Aimable
        )
        for (use_item, inventory, stats) in self.get_player_item():
            for item, (_, _) in scroll_components:
                if use_item == item:
                    self.scene.action = {'target_with': item}


class UpdateDropInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_player_item(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Inventory,
            c.Position
        )
        for _, (_, inventory, pos) in iterable:
            index = int(self.scene.action.get('inventory_index'))
            if index < len(inventory.items):
                drop_item = inventory.items[index]
                yield (drop_item, inventory, pos)

    def get_drop_item(self):
        iterable = self.world.get_components(
            c.Carryable,
            c.Describable
        )
        for (drop_item, inventory, pos) in self.get_player_item():
            for item, (_, desc) in iterable:
                if drop_item == item:
                    yield (item, inventory, pos, desc)

    def process(self, *args):
        if self.scene.action.get('inventory_index'):
            for item, inventory, pos, desc in self.get_drop_item():
                inventory.items.remove(item)
                self.world.add_component(item, c.Position(x=pos.x, y=pos.y))
                self.scene.message.append(
                    ('You dropped the {0}'.format(desc.name), tcod.yellow)
                )
