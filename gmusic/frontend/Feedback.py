from gmusic.frontend.CursedObject import CursedObject
import curses

class Feedback(CursedObject):
    """Used for providing quick feedback to the user"""

    def __init__(self, screen):
        self.screen = screen

    def draw(self, information):
        self.center_text(information, self.height() - 2)
