import esper


class RenderMap(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):
        if self.scene.action.get('reveal_all'):
            self.scene.game_map.explored[:] = True

        if self.scene.fov_recompute:
            game_map = self.scene.game_map
            con = self.scene.con

            light_ground = (game_map.ch == 249) & game_map.fov
            con.ch[light_ground] = game_map.ch[light_ground]
            con.fg[light_ground] = game_map.fg[light_ground]
            con.bg[light_ground] = game_map.bg[light_ground]

            light_wall = (game_map.ch == 176) & game_map.fov
            con.ch[light_wall] = game_map.ch[light_wall]
            con.fg[light_wall] = game_map.fg[light_wall]
            con.bg[light_wall] = game_map.bg[light_wall]

            light_roof = (game_map.ch == 219) & game_map.fov
            con.ch[light_roof] = game_map.ch[light_roof]
            con.fg[light_roof] = game_map.fg[light_roof]
            con.bg[light_roof] = game_map.bg[light_roof]

            dark_ground = (game_map.ch == 249) & ~game_map.fov & game_map.explored
            con.ch[dark_ground] = 249
            con.fg[dark_ground] = (45, 40, 35)
            con.bg[dark_ground] = (30, 20, 10)

            dark_wall = (game_map.ch == 176) & ~game_map.fov & game_map.explored
            con.ch[dark_wall] = 176
            con.fg[dark_wall] = (60, 55, 50)
            con.bg[dark_wall] = (30, 20, 10)

            dark_roof = (game_map.ch == 219) & ~game_map.fov & game_map.explored
            con.ch[dark_roof] = 219
            con.fg[dark_roof] = (60, 55, 50)
            con.bg[dark_roof] = (30, 20, 10)

            con.ch[~game_map.explored] = 219
            con.fg[~game_map.explored] = (15, 10, 5)
            con.bg[~game_map.explored] = (15, 10, 5)
