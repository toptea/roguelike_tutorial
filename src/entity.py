import component as c


def player(x, y):
    return (
        c.IsPlayer(),
        c.Position(x=x, y=y),
        c.Velocity(),
        c.Renderable('@'),
        c.Collidable(),
        c.Describable(),
        c.Health(),
        c.Stats(),
    )


def monster(char, fg, x, y):
    return (
        c.IsHostile(),
        c.Position(x=x, y=y),
        c.Velocity(),
        c.Renderable(char=char, fg=fg),
        c.Collidable(),
        c.Describable(),
        c.Health(),
        c.Stats(),
    )
