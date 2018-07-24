from .targeting import UpdateTargeting
from .level_up import UpdateLevelUp
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .experience import Experience
from .stairs import TakeStairs
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
    InputTargeting
)

from .inventory import (
    UpdateUseInventory,
    UpdateDropInventory,
)

from .state import (
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory,
    StateTitle,
    StateLevelUp,
    StateCharacterScreen,
    StateTargeting
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
    'targeting': [
        RenderPanel(),
        RenderConsole(),
        InputTargeting(),
        UpdateTargeting(),
        Death(),
        StateTargeting(),
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
