import component as c

import esper
import tcod


class Status(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_enemies(self):
        iterable = self.world.get_components(
            c.EnemyTurn,
            c.Stats,
            c.Status,
            c.Describable
        )
        for _, (_, stats, status, desc) in iterable:
            yield (stats, status, desc)

    def process(self, *args):
        for stats, status, desc in self.get_enemies():
            if status.countdown <= 0:
                status.confuse = False
                status.paralyse = False
                status.freeze = False
                status.burn = False

            if status.confuse:
                self.scene.message.append(
                    ('{} is confused!'.format(desc.name), tcod.orange)
                )
            if status.paralyse:
                self.scene.message.append(
                    ('{} is paralysed!'.format(desc.name), tcod.orange)
                )
            if status.freeze:
                self.scene.message.append(
                    ('{} is frozen!'.format(desc.name), tcod.orange)
                )
            if status.burn:
                stats.hp -= 5
                self.scene.message.append(
                    ('{} is burning, dealing 5 damage!'.format(desc.name), tcod.orange)
                )
            status.countdown -= 1
