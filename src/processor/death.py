import component as c
import const
import esper
import tcod


class Death(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_dead_entities(self):
        iterable = self.world.get_components(
            c.Renderable,
            c.Describable,
            c.Stats
        )
        for ent, (rend, desc, stats) in iterable:
            if stats.hp <= 0:
                yield (ent, rend, desc, stats)

    def process(self, *args):
        for ent, rend, desc, stats in self.get_dead_entities():
            rend.char = '%'
            rend.fg = tcod.dark_red
            rend.layer = const.LAYER_CORPSE
            self.try_removing(ent, c.Collidable)
            self.try_removing(ent, c.Stats)
            self.try_removing(ent, c.Movable)
            self.try_removing(ent, c.PlayerTurn)
            self.try_removing(ent, c.EnemyTurn)
            self.scene.message.append(
                ('{} is dead!'.format(desc.name.capitalize()), tcod.orange)
            )

    def try_removing(self, entity, component):
        if self.world.has_component(entity, component):
            self.world.remove_component(entity, component)
