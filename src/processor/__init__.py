from .render import RenderConsole, RenderPanel, RenderMenu, RenderTitle
from .input_handler import InputPlayer, InputInventory, InputTitle
from .item import UseItem, DropItem
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .stairs import TakeStairs
from .console import Console
from .pickup import PickUp
from .death import Death
from .fov import FOV


from .state import (
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory,
    StateTitle
)


PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        RenderConsole(),
        InputPlayer(),
        MovePlayer(),
        Death(),
        PickUp(),
        TakeStairs(),
        Console(),
        RenderPanel(),
        StatePlayerTurn()
    ],
    'enemy_turn': [
        MoveEnemy(),
        Death(),
        StateEnemyTurn(),
    ],
    'show_inventory': [
        RenderPanel(),
        RenderMenu('show'),
        InputInventory(),
        UseItem(),
        StateShowInventory()
    ],
    'drop_inventory': [
        RenderPanel(),
        RenderMenu('drop'),
        InputInventory(),
        DropItem(),
        StateDropInventory()
    ],
    'target': [
        RenderPanel(),
        # InputTargeting(),
        # Targeting(),
    ],
}
