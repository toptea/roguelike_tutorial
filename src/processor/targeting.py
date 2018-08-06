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
            c.StatusModifier,
            c.Describable
        )

        for item, (_, _, stats_mod, status_mod, item_desc) in iterable:
            if self.scene.action.get('target_with')[0] == item:
                yield (item, stats_mod, status_mod, item_desc)

    def get_inventory(self):
        inventory = self.scene.action.get('target_with')[1]
        inventory.items.sort()
        return inventory

    def get_target(self):
        x, y = self.scene.action.get('left_click')
        iterable = self.world.get_components(
            c.Position,
            c.Stats,
            c.Status,
            c.Describable
        )
        for _, (pos, target_stats, target_status, target_desc) in iterable:
            if pos.x == x and pos.y == y:
                if self.scene.game_map.fov[pos.y, pos.x]:
                    yield (target_stats, target_status, target_desc)

    def process(self, *args):

        if self.scene.action.get('left_click'):
            for target_stats, target_status, target_desc in self.get_target():
                for item, stats_mod, status_mod, item_desc in self.get_scroll():
                    target_stats.hp += stats_mod.hp
                    if target_stats.hp > target_stats.max_hp:
                        target_stats.hp = target_stats.max_hp

                    if stats_mod.hp > 0:
                        self.scene.message.append(
                            (
                                '{} heal {}, recovering {} HP!'.format(
                                    item_desc.name,
                                    target_desc.name,
                                    stats_mod.hp
                                )
                                , tcod.orange
                            )
                        )
                    else:
                        self.scene.message.append(
                            (
                                '{} hit {}, dealing {} damage!'.format(
                                    item_desc.name,
                                    target_desc.name,
                                    stats_mod.hp
                                )
                                , tcod.orange
                            )
                        )
                    if status_mod.countdown > 0:
                        target_status.countdown = status_mod.countdown
                        target_status.confuse = status_mod.confuse
                        target_status.paralyse = status_mod.paralyse
                        target_status.freeze = status_mod.freeze
                        target_status.burn = status_mod.burn

                    inventory = self.get_inventory()
                    inventory.items.remove(item)
                    self.world.delete_entity(item)

                    self.scene.action = {'hit_target': True}
                    return
            else:
                self.scene.action['left_click'] = None
                self.scene.message.append(
                    ('There is no targetable enemy at that location', tcod.yellow)
                )

