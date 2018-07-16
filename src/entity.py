import component as c
import const
import tcod


def player(x, y):
    return (
        c.IsPlayer(),
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
        c.IsHostile(),
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
