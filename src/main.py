import processor
import dungeon.level
import input_handler
import esper
import tcod


class Scene:

    def __init__(self):
        self.event_processor = input_handler.EventProcessor()
        self.event = input_handler.Event({})
        self.level = dungeon.level.MainLevel()
        self.world = esper.World()

    def on_start(self):
        processors = (
            # processor.FOV(),
            processor.Render(),
            processor.Movement(),
            processor.Console()
        )
        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)

    def on_enter(self):
        self.level.make_map()
        self.level.place_entities()
        for entity in self.level.entities:
            if len(entity) <= 1:
                self.world.create_entity(entity)
            else:
                self.world.create_entity(*entity)

    def on_input(self):
        self.event.action = self.event_processor.process()

    def on_update(self):
        self.world.process(
            self.event,
            self.level.game_map
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
