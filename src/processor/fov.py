import esper
import component as c
import tcod
import const


class FOV(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        _, game_map = next(self.world.get_component(c.GameMap))
        for _, (pos, event) in self.world.get_components(c.Position, c.Event):
            if event.fov_recompute:
                tcod.map_compute_fov(
                    game_map,
                    x=pos.x,
                    y=pos.y,
                    radius=const.FOV_RADIUS,
                    light_walls=const.FOV_LIGHT_WALLS,
                    algo=const.FOV_ALGORITHM,
                )

                game_map.explored[game_map.fov] = True
