import component as c

import esper
import tcod


class Death(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        for ent, (rend, desc, stats) in self.world.get_components(c.Renderable, c.Describable, c.Stats):
            if stats.hp <= 0:
                rend.char = '%'
                rend.fg = tcod.dark_red
                self.scene.message.append('{} is dead!'.format(desc.name.capitalize()))
                self.world.remove_component(ent, c.Collidable)
                self.world.remove_component(ent, c.Stats)
                self.world.remove_component(ent, c.Velocity)



