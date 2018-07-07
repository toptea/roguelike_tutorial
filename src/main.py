import tcod
import const
import scene


class SceneManager:

    def __init__(self, state='game'):
        tcod.console_set_custom_font(
            fontFile=const.FONT_PATH,
            flags=const.FONT_FLAG
        )
        self.root_console = tcod.console_init_root(
            w=const.SCREEN_WIDTH,
            h=const.SCREEN_HEIGHT,
            title=const.TITLE
        )
        self.scenes = {
            'menu': scene.MainMenu(),
            'option': scene.Option(),
            'game': scene.Game(),
        }
        self.current_scene = self.scenes[state]
        scene.Scene.manager = self

    def change_scene(self, state):
        self.current_scene = self.scenes[state]

    def randomize_scene(self):
        self.current_scene = scene.Game()

    def run(self):
        while not tcod.console_is_window_closed():
            self.current_scene.update()


if __name__ == '__main__':
    app = SceneManager(state='game')
    app.run()
