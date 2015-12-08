from gmusic.model.Event import Event

class PlayOrStop(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.track = None
