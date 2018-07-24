from .inventory import UseInventory, DropInventory
from .experience import Experience
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .stairs import TakeStairs
from .level_up import LevelUp
from .console import Console
from .pickup import PickUp
from .death import Death
from .fov import FOV



from .render import (
    RenderConsole,
    RenderPanel,
    RenderInventory,
    RenderTitle,
    RenderLevelUp
)

from .input_handler import (
    InputPlayer,
    InputInventory,
    InputTitle,
    InputLevelUp
)

from .state import (
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory,
    StateTitle,
    StateLevelUp,
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
        UseInventory(),
        StateShowInventory()
    ],
    'drop_inventory': [
        RenderPanel(),
        RenderInventory('drop'),
        InputInventory(),
        DropInventory(),
        StateDropInventory()
    ],
    'target': [
        RenderPanel(),
        # InputTargeting(),
        # Targeting(),
    ],
    'level_up': [
        RenderPanel(),
        RenderLevelUp(),
        InputLevelUp(),
        LevelUp(),
        StateLevelUp(),
    ]
}
