from .experience import Experience
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .stairs import TakeStairs
from .level_up import UpdateLevelUp
from .console import Console
from .pickup import PickUp
from .death import Death
from .fov import FOV

from .render import (
    RenderConsole,
    RenderPanel,
    RenderInventory,
    RenderTitle,
    RenderLevelUp,
    RenderCharacterScreen,
)

from .input_handler import (
    InputPlayer,
    InputInventory,
    InputTitle,
    InputLevelUp,
    InputCharacterScreen,
)

from .inventory import (
    UpdateUseInventory,
    UpdateDropInventory
)

from .state import (
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory,
    StateTitle,
    StateLevelUp,
    StateCharacterScreen,
)


PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        RenderConsole(),
        InputPlayer(),
        MovePlayer(),
        Experience(),
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
        RenderInventory('show'),
        InputInventory(),
        UpdateUseInventory(),
        StateShowInventory()
    ],
    'drop_inventory': [
        RenderPanel(),
        RenderInventory('drop'),
        InputInventory(),
        UpdateDropInventory(),
        StateDropInventory()
    ],
    'target': [
        RenderPanel(),
        # InputTargeting(),
        # Targeting(),
    ],
    'level_up': [
        # RenderPanel(),
        RenderLevelUp(),
        InputLevelUp(),
        UpdateLevelUp(),
        StateLevelUp(),
    ],
    'character_screen': [
        RenderCharacterScreen(),
        InputCharacterScreen(),
        StateCharacterScreen(),
    ]
}
