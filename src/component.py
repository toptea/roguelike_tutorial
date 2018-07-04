from dataclasses import dataclass
import tcod
import esper


@dataclass
class IsPlayer:
    pass


@dataclass
class EnemyAI:
    pass


@dataclass
class Position:
    x: int
    y: int
    blocks: bool = True


@dataclass
class Fighter:
    max_hp: int
    hp: int
    defense: int
    power: int


@dataclass
class Velocity:
    dx: int
    dy: int


@dataclass
class Renderable:
    char: str = '@'
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    bg_blend: int = tcod.BKGND_NONE


@dataclass
class Collidable:
    pass


@dataclass
class Describable:
    name: str


class FOV(esper.Processor):
    pass


class PlayerAction(esper.Processor):
    pass


class PlayerShowInventoryAction(esper.Processor):
    pass


class PlayerDropInventoryAction(esper.Processor):
    pass


class PlayerTargetingAction(esper.Processor):
    pass


class EnemyAction(esper.Processor):
    pass


class ConsoleAction(esper.Processor):
    pass


class Render(esper.Processor):
    pass


class MoveAttack(esper.Processor):
    pass


class Collision(esper.Processor):
    pass


class Pickup(esper.Processor):
    pass


class MessageLog(esper.Processor):
    pass


class StateManager(esper.Processor):
    pass


class GameOver(esper.Processor):
    pass
