import component as c

import esper


class UpdateLevelUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        level_up = self.scene.action.get('level_up')
        if level_up:
            for _, (_, stats) in self.world.get_components(c.PlayerTurn, c.Stats):
                if level_up == 'hp':
                    stats.max_hp += 20
                    stats.hp += 20
                elif level_up == 'str':
                    stats.power += 1
                elif level_up == 'def':
                    stats.defense += 1
