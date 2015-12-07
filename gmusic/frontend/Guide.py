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
        first_line = \
            "      ↕: Nav     "+\
            "  ↔ : Page     " +\
            "  -: Vol Down  "+\
            " +: Vol Up     "
        second_line = \
            "  q: Queue    "+\
            "Spc: ▶/▌▌     "+\
            "  n: Next     " +\
            "  p: Prev "
        third_line = \
            "  i: CLI      "+\
            "  r: Radio     "

        return (first_line, second_line, third_line)
