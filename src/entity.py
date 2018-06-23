import component as c
import const


def game_map():
    return c.GameMap(width=const.MAP_WIDTH, height=const.MAP_HEIGHT)


def player(x=40, y=20):
    return (
        c.Renderable('@'),
        c.Position(x=x, y=y),
        c.IsPlayer(),
    )


def monster(char, fg, x, y):
    return (
        c.Renderable(char=char, fg=fg),
        c.Position(x=x, y=y)
    )
