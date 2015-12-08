# -*- coding: utf-8 -*-
from gmusic.frontend.CursedObject import CursedObject
import curses

class Guide(CursedObject):
    """Displays quick shortcuts at the bottom of the screen"""

    def __init__(self, screen):
        self.screen = screen


    def draw(self):
        lines = self.keys()

        for i in range(3):
            self.center_text(lines[i], self.height() - (5-i))

    def keys(self):
        line1 = "↕ : Move Selection    r : Create Radio    n : Next    + : Vol Up  "
        line2 = "↔ : Change Page       q : Play Next       p : Prev    - : Vol Down"
        # offset last row to account for wierd centering issues
        line3 = "                        i : CLI         Space : ▶/❚❚              "

        return (line1, line2, line3)
