import component as c

import esper


class BlankProcessor(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self, *args):
        print('blank')
