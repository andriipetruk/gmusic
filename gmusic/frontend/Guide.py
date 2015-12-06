# -*- coding: utf-8 -*-
from gmusic.frontend.CursedObject import CursedObject
import curses

class Guide(CursedObject):
    """Displays quick shortcuts at the bottom of the screen"""

    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        first_line = \
            "  ↕ : Nav      "+\
            " ↔ : Page     " +\
            "  n: Next     " +\
            "  p: Prev "
        second_line = \
            "Spc: ▶/||     "+\
            "  q: Queue    "+\
            "  i: Cmd Line "+\
            "  r: Radio"

        self.center_text(first_line, self.height() - 4)
        self.center_text(second_line, self.height() - 3)
