import component as c

import esper


class MessageLog(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        while self.scene.message:
            print(self.scene.message.popleft())
