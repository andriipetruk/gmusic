from gmusic.model.Event import Event

class ChangeMenu(Event):
    def __init__(self, sender):
        Event.__init__(self, sender)
        self.menu_type = "main_menu"
