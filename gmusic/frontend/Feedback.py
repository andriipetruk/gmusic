from gmusic.frontend.CursedObject import CursedObject
import curses

class Feedback(CursedObject):
    """Used for providing quick feedback to the user"""

    def __init__(self, screen):
        self.screen = screen
        self.is_visible = False

    def draw(self):
        if not self.is_visible:
            return

        height, width = self.screen.getmaxyx()
        win = curses.newwin(3, 3, 3, 3)
