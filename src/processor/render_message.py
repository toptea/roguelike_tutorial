import textwrap
import esper
import const
import tcod


class RenderMessage(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()
        self.display_message = []
        self.width = const.MESSAGE_WIDTH
        self.height = const.MESSAGE_HEIGHT
        self.x = const.MESSAGE_X

    def process(self, *args):
        while self.scene.message:
            message, color = self.scene.message.popleft()
            new_msg_lines = textwrap.wrap(message, self.width)
            print(message)

            for line in new_msg_lines:
                if len(self.display_message) == self.height:
                    self.display_message.pop(0)
                self.display_message.append((line, color))

        for y, (message, color) in enumerate(self.display_message):
            self.scene.panel.default_fg = color
            self.scene.panel.print_(
                x=self.x,
                y=y+1,
                string=message,
                bg_blend=tcod.BKGND_NONE,
                alignment=tcod.LEFT
            )
