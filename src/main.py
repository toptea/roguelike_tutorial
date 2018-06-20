import processor as p
import entity as e

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
        self.world.create_entity(e.test_map())
        self.world.create_entity(*e.player(x=10, y=20))
        self.world.create_entity(*e.monster(char='M', fg=tcod.red, x=20, y=20))

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
