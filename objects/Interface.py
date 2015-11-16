from objects.ContentManager import ContentManager
from objects.CursedMenu import CursedMenu

class Interface(object):
    """This is the command line interface. It handles
    all user input and sends to the processor as necessary"""

    def __init__(self):
        """Initialization"""
        self.content_manager = ContentManager()
        self.display = CursedMenu(self.content_manager)

    def __start__(self):
        """Our default running loop which governs the UI"""
        self.content_manager.load()
        self.display.start()
