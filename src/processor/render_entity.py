import component as c

import esper


class RenderEntity(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        list_c = list(self.world.get_components(c.Renderable, c.Position))
        list_c.sort(key=lambda row: row[1][0].layer)
        for _, (rend, pos) in list_c:
            if self.scene.game_map.fov[pos.y, pos.x]:
                self.scene.con.default_fg = rend.fg
                self.scene.con.default_bg = rend.bg
                self.scene.con.print_(
                    x=pos.x,
                    y=pos.y,
                    string=rend.char,
                    bg_blend=rend.bg_blend
                )


class ClearEntity(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        generator = self.world.get_components(c.Renderable, c.Position)
        for _, (rend, pos) in generator:
            self.scene.con.print_(
                x=pos.x,
                y=pos.y,
                string=' ',
                bg_blend=rend.bg_blend
            )
