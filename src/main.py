import processor
import level
import input_handler
import esper
import tcod


class Scene:

    def __init__(self):
        self.event_processor = input_handler.EventProcessor()
        self.event = input_handler.Event({})
        self.level_ = level.MainLevel()
        self.world = esper.World()

    def on_start(self):
        processors = (
            processor.FOV(),
            processor.Render(),
            processor.Movement(),
            processor.Console()
        )
        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)

    def on_enter(self):
        self.level_.make_map()
        self.level_.place_entities()
        self.level_.add_to_world(self.world)

    def on_input(self):
        self.event.action = self.event_processor.process()

    def on_update(self):
        self.world.process(
            self.event,
            self.level_.game_map
        )


def main():
    scene = Scene()
    scene.on_start()
    scene.on_enter()
    while not tcod.console_is_window_closed():
        scene.on_input()
        scene.on_update()


if __name__ == '__main__':
    main()
