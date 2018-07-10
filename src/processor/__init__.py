from .render import Render
from .move_player import MovePlayer
from .console import Console
from .fov import FOV
from .input_player import InputPlayer
from .move_enemy import MoveEnemy
from .message_log import MessageLog
from .death import Death
from .manage_state import ManageState

PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        Render(),
        InputPlayer(),
        MovePlayer(),
        MoveEnemy(),
        Death(),
        MessageLog(),
        Console(),

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
