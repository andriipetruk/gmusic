from gmusic.model.Event import Event

class Search(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.results = []
        self.title = "No Title"
        self.display_element_type = "No elements"
