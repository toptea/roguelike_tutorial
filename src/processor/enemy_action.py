import component as c

import esper


class EnemyAction(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        print('The enemies ponders the meaning of its existence')
        self.scene.change_processors('player_turn')
