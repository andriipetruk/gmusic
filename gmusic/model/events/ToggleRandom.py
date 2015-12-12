from gmusic.model.Event import Event

class ToggleRandom(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.is_random = False
