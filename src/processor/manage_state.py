import esper


class ManageState(esper.Processor):
    scene = None

    def __init__(self, state):
        super().__init__()
        self.state = state

    def process(self, *args):
        if self.scene.action != {}:
            if self.state == 'player_turn' and self.scene.state == 'player_turn':
                self.scene.change_processors('enemy_turn')
            if self.state == 'enemy_turn' and self.scene.state == 'enemy_turn':
                self.scene.change_processors('player_turn')
            if self.state == 'game_over' and self.scene.state == 'game_over':
                self.scene.change_processors('game_over')
