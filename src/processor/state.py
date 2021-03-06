import esper
import tcod


class StatePlayerTurn(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:

            if all(key in ['move', 'pickup'] for key in self.scene.action.keys()):
                self.scene.change_processors('enemy_turn')

            if self.scene.action.get('show_inventory'):
                self.scene.change_processors('show_inventory')

            if self.scene.action.get('drop_inventory'):
                self.scene.change_processors('drop_inventory')

            if self.scene.action.get('next_level'):
                player = self.scene.action.get('next_level')[0]
                inventory = self.scene.action.get('next_level')[1]
                self.scene.manager.next_level(
                    player_entity=player,
                    item_entities=inventory
                )

            if self.scene.action.get('show_level_up'):
                self.scene.change_processors('level_up')

            if self.scene.action.get('show_character_screen'):
                self.scene.change_processors('character_screen')


class StateEnemyTurn(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        self.scene.change_processors('player_turn')


class StateShowInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:
            if self.scene.action.get('target_with'):
                self.scene.message.append(
                    ('Please select a target using the mouse'.format(), tcod.blue)
                )
                self.scene.change_processors('targeting')
            if self.scene.action.get('exit'):
                self.scene.change_processors('player_turn')


class StateDropInventory(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:
            if self.scene.action.get('exit'):
                self.scene.change_processors('player_turn')


class StateTitle(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:

            if self.scene.action.get('new_game'):
                self.scene.manager.change_scene('game')

            if self.scene.action.get('load_game'):
                self.scene.manager.load_game()


class StateLevelUp(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:
            if self.scene.action.get('level_up'):
                self.scene.change_processors('player_turn')


class StateCharacterScreen(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:
            if self.scene.action.get('exit'):
                self.scene.change_processors('player_turn')


class StateTargeting(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action != {}:
            if self.scene.action.get('exit'):
                self.scene.action = {}
                self.scene.change_processors('show_inventory')
            if self.scene.action.get('hit_target'):
                self.scene.change_processors('enemy_turn')
