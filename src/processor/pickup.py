import component as c

import esper


class PickUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action.get('pickup'):
            for player, (_, player_pos) in self.world.get_components(c.IsPlayer, c.Position):
                for item, (_, item_pos) in self.world.get_components(c.Carryable, c.Position):
                    if player_pos.x == item_pos.x and player_pos.y == item_pos.y:
                        if self.world.has_component(item, c.Renderable):
                            self.world.remove_component(item, c.Renderable)
