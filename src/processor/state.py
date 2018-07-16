import esper


class StateRenderTurn(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        self.scene.change_processors('player_turn')


class StatePlayerTurn(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action != {}:

            if all(key in ['move', 'pickup'] for key in self.scene.action.keys()):
                self.scene.change_processors('enemy_turn')

            if self.scene.action.get('show_inventory'):
                self.scene.change_processors('show_inventory')

            if self.scene.action.get('drop_inventory'):
                self.scene.change_processors('drop_inventory')


class StateEnemyTurn(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        self.scene.change_processors('render_all')


class StateShowInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action != {}:
            if self.scene.action.get('exit'):
                self.scene.change_processors('render_all')
            else:
                self.scene.change_processors('show_inventory')


class StateDropInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        if self.scene.action != {}:
            if self.scene.action.get('exit'):
                self.scene.change_processors('render_all')
            else:
                self.scene.change_processors('drop_inventory')
