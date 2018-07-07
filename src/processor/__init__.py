from .render import Render
from .move_attack import MoveAttack
from .console import Console
from .fov import FOV
from .player_action import PlayerAction
from .enemy_action import EnemyAction


PROCESSOR_GROUP = {
    'player_turn': [
        FOV(),
        PlayerAction(),
        Render(),
        # UnderStatus(),
        MoveAttack(),
        # PickUp(),
        # Enter(),
        # Death(),
        # MessageLog(),
        Console()
    ],
    'enemy_turn': [
        EnemyAction(),
        Render(),
        # UnderStatus(),
        # MoveAttack(),
        # Death(),
        # MessageLog(),
    ],
    'show_inventory': [
        # InventoryAction(),
        # UseHealthItem(),
        # UseStatsItem(),
        # UseStatusItem(),
        # Equip(),

    ],
    'drop_inventory': [
        # InventoryAction(),
        # Drop(),
    ],
    'target': [
        # TargetAction(),
        # Targeting(),
    ],
}


"""
# Player or Enemy Turn
from .fov import FOV


from .render import Render
from .collision import Collision
from .move_attack import MoveAttack
from .pickup import Pickup
from .enter import Enter
from .death import Death
from .message_log import MessageLog

# Show or Drop Inventory
from .inventory_action import InventoryAction
from .use_health_item import UseHealthItem
from .use_stats_item import UseStatsItem
from .use_status_item import UseStatusItem
from .equip import Equip
from .drop import Drop

# Targeting
from .target_action import TargetAction
from .targeting import Targeting
"""