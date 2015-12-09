from gmusic.model.Event import Event

class Random(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.is_random = False
