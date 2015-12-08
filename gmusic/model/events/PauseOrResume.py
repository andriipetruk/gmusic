from gmusic.model.Event import Event

class PauseOrResume(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.is_playing = True
