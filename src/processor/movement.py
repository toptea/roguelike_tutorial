import component as c

import esper


class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (pos, event) in self.world.get_components(c.Position, c.Event):
            move = event.action.get('move')
            if move:
                dx, dy = move
                pos.x += dx
                pos.y += dy
