import component as c

import esper
import tcod


class UpdateTargeting(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_scroll(self):
        iterable = self.world.get_components(
            c.Carryable,
            c.Aimable,
            c.StatsModifier,
            c.StatusModifer,
            c.Describable
        )
        for item, (_, _, stats_mod, item_desc) in iterable:
            if self.scene.action.get('target_with') == item:
                yield (item, stats_mod, item_desc)

    def get_inventory(self):
        iterable = self.world.get_components(
            c.PlayerTurn,
            c.Inventory,
        )
        for _, (_, inventory) in iterable:
            yield inventory

    def get_target(self):
        x, y = self.scene.action.get('left_click')
        iterable = self.world.get_components(
            c.Position,
            c.Stats,
            c.Status,
            c.Describable
        )
        for _, (pos, target_stats, target_desc) in iterable:
            if pos.x == x and pos.y == y:
                if self.scene.game_map.fov[pos.y, pos.x]:
                    yield (target_stats, target_desc)

    def process(self, *args):
        if self.scene.action.get('left_click'):
            for target_stats, target_desc in self.get_target():
                for item, stats_mod, item_desc in self.get_scroll():
                    target_stats.hp += stats_mod.hp
                    self.scene.message.append(
                        ('The missile hit {}, dealing {} damage!'.format(target_desc.name, abs(stats_mod.hp)), tcod.orange)
                    )
                    for inventory in self.get_inventory():
                        inventory.items.remove(item)
                        self.world.delete_entity(item)

                    self.scene.action = {'hit_target': True}
            else:
                self.scene.action['left_click'] = None
                self.scene.message.append(
                    ('There is no targetable enemy at that location', tcod.yellow)
                )
