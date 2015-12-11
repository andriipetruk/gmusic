from gmusic.model.Event import Event

class Search(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.state = None
