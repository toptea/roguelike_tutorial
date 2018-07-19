from .render import RenderConsole, RenderPanel, RenderMenu
from .input_handler import InputPlayer, InputInventory
from .item import UseItem, DropItem
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .console import Console
from .pickup import PickUp
from .death import Death
from .fov import FOV

from .state import (
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory
)


PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        RenderPanel(),
        RenderConsole(),
        InputPlayer(),
        MovePlayer(),
        Death(),
        PickUp(),
        # Enter(),
        Console(),
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
