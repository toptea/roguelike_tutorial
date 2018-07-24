import component as c
import const
import tcod


def player(x, y):
    return (
        c.PlayerTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable('@'),
        c.Collidable(),
        c.Describable(name='player'),
        c.Stats(max_hp=30, hp=15, defense=2, power=5),
        c.Inventory([]),
    )


def monster(char, fg, x, y):
    return (
        c.EnemyTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable(char=char, fg=fg),
        c.Collidable(),
        c.Describable(name='monster'),
        c.Stats(hp=10, defense=0, power=3),
    )


def healing_potion(x, y):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char='!', fg=tcod.fuchsia, layer=const.LAYER_ITEM),
        c.Describable(name='healing potion'),
        c.Carryable(),
        c.Consumable(),
        c.StatsModifier(hp=10)
    )


def scroll(x, y):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char='!', fg=tcod.orange, layer=const.LAYER_ITEM),
        c.Describable(name='fire'),
        c.Carryable(),
        c.Aimable(),
        c.StatsModifier(hp=-10)
    )
