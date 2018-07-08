from .render import Render
from .move_player import MovePlayer
from .console import Console
from .fov import FOV
from .event_ingame import EventInGame
from .move_enemy import MoveEnemy
from .message_log import MessageLog
from .death import Death
from .manage_state import ManageState

PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        EventInGame(),
        MovePlayer(),
        # PickUp(),
        # Enter(),
        Console(),
        ManageState('player_turn')
    ],
    'enemy_turn': [
        MoveEnemy(),
        Death(),
        MessageLog(),
        Render(),
        ManageState('enemy_turn')
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
    'game_over': [
        EventInGame(),
        Render(),
        Console(),
        ManageState('game_over')
    ]
}
