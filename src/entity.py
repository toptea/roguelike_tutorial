import component as c


def player(x, y):
    return (
        c.IsPlayer(),
        c.Position(x=x, y=y),
        c.Velocity(),
        c.Renderable('@'),
        c.RenderOrderActor(),
        c.Collidable(),
        c.Describable(name='player'),
        c.Stats(max_hp=30, hp=30, defense=2, power=5),
    )


def monster(char, fg, x, y):
    return (
        c.IsHostile(),
        c.Position(x=x, y=y),
        c.Velocity(),
        c.Renderable(char=char, fg=fg),
        c.RenderOrderActor(),
        c.Collidable(),
        c.Describable(name='monster'),
        c.Stats(hp=10, defense=0, power=3),
    )
