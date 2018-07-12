from .render_entity import RenderEntity, ClearEntity
from .render_message import RenderMessage
from .render_reset import RenderReset
from .render_map import RenderMap
from .render_ui import RenderUI

from .input_console import InputConsole
from .input_player import InputPlayer
from .move_player import MovePlayer
from .move_enemy import MoveEnemy

from .death import Death
from .fov import FOV


PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        RenderMap(),
        RenderEntity(),
        RenderUI(),
        RenderMessage(),
        RenderReset(),
        ClearEntity(),

        InputPlayer(),
        InputConsole(),

        MovePlayer(),
        MoveEnemy(),
        Death(),

        # PickUp(),
        # Enter(),
        # ManageState('player_turn')
    ],
    'enemy_turn': [
        # ManageState('enemy_turn')
    ],
    'show_inventory': [
        # EventShowInventory(),
        # UseHealthItem(),
        # UseStatsItem(),
        # UseStatusItem(),
        # Equip(),
    ],
    'drop_inventory': [
        # EventDropInventory(),
        # Drop(),
    ],
    'target': [
        # TargetAction(),
        # Targeting(),
    ],
}
