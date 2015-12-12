from gmusic.model.Event import Event

class Feedback(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.message = "Default Message"
        self.duration = 2.0
        self.is_showing_message = True
