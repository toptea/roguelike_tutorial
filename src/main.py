import processor as p
import level

import esper
import tcod


class Scene:

    def __init__(self):
        self.world = esper.World()

    def on_start(self):
        processors = (
            p.RenderProcessor(),
            p.EventProcessor(),
            p.MovementProcessor(),
            p.ConsoleProcessor()
        )
        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)

    def on_enter(self):
        lvl = level.PillarRoomTest()
        lvl.make_map()
        lvl.place_entities()
        lvl.add_to_world(self.world)

    def on_update(self):
        self.world.process()


def main():
    scene = Scene()
    scene.on_start()
    scene.on_enter()
    while not tcod.console_is_window_closed():
        scene.on_update()


if __name__ == '__main__':
    main()
