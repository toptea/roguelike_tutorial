import esper
import component as c
import tcod
import const


class FOV(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        for _, (_, pos) in self.world.get_components(c.IsPlayer, c.Position):
            if self.scene.fov_recompute:
                tcod.map_compute_fov(
                    self.scene.game_map,
                    x=pos.x,
                    y=pos.y,
                    radius=const.FOV_RADIUS,
                    light_walls=const.FOV_LIGHT_WALLS,
                    algo=const.FOV_ALGORITHM,
                )
                fov_bool_array = self.scene.game_map.fov
                self.scene.game_map.explored[fov_bool_array] = True
