import component as c
import const


def test_map():
    game_map = c.GameMap(width=const.MAP_WIDTH, height=const.MAP_HEIGHT)
    game_map.transparent[:] = True
    game_map.transparent[::3, 2::3] = False
    game_map.transparent[:, 0::const.MAP_WIDTH-1] = False
    game_map.transparent[0::const.MAP_HEIGHT-1, :] = False
    game_map.walkable[:] = game_map.transparent[:]
    return game_map


def player(x=40, y=20):
    return (
        c.Renderable('@'),
        c.Position(x, y),
        c.Event({}),
    )


def monster(char, fg, x, y):
    return (
        c.Renderable(char=char, fg=fg),
        c.Position(x=x, y=y)
    )
