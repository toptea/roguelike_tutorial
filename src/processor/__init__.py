from .render import Render
from .move_player import MovePlayer
from .console import Console
from .fov import FOV
from .event_ingame import EventInGame
from .move_enemy import MoveEnemy
from .message_log import MessageLog
from .death import Death


PROCESSOR_GROUP = {
    'player_turn': [
        Render(),
        FOV(),
        EventInGame(),
        # UnderStatus(),
        MovePlayer(),
        # PickUp(),
        # Enter(),
        Death(),
        MessageLog(),
        Console()
    ],
    'enemy_turn': [
        MoveEnemy(),
        # UnderStatus(),
        # MoveAttack(),
        # Death(),
        # MessageLog(),
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


"""
# Player or Enemy Turn
from .pickup import Pickup
from .enter import Enter
from .death import Death


# Show or Drop Inventory
from .event_inventory import EventInventory
from .use_health_item import UseHealthItem
from .use_stats_item import UseStatsItem
from .use_status_item import UseStatusItem
from .equip import Equip
from .drop import Drop

# Targeting
from .target_action import TargetAction
from .targeting import Targeting
"""