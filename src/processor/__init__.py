from .render_entity import RenderEntity, ClearEntity
from .render_message import RenderMessage
from .render_reset import RenderReset
from .render_map import RenderMap
from .render_ui import RenderUI

from .input_handler import InputPlayer, InputInventory
from .move_player import MovePlayer
from .move_enemy import MoveEnemy
from .console import InputConsole
from .pickup import PickUp
from .death import Death
from .fov import FOV

from .state import (
    StateRenderTurn,
    StateEnemyTurn,
    StatePlayerTurn,
    StateShowInventory,
    StateDropInventory
)

PROCESSOR_GROUP = {
    'render_all': [
        FOV(),
        RenderMap(),
        RenderEntity(),
        RenderUI(),
        RenderMessage(),
        RenderReset(),
        ClearEntity(),
        StateRenderTurn()
    ],
    'player_turn': [
        InputPlayer(),
        InputConsole(),
        MovePlayer(),
        Death(),
        PickUp(),
        # Enter(),
        StatePlayerTurn()
    ],
    'enemy_turn': [
        MoveEnemy(),
        Death(),
        StateEnemyTurn(),
    ],
    'show_inventory': [
        InputInventory(),
        # UseHealthItem(),
        # UseStatsItem(),
        # UseStatusItem(),
        # Equip(),
        StateShowInventory()
    ],
    'drop_inventory': [
        InputInventory(),
        # Drop(),
        StateDropInventory()
    ],
    'target': [
        # TargetAction(),
        # Targeting(),
    ],
}
