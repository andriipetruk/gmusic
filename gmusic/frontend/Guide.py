# -*- coding: utf-8 -*-
from gmusic.frontend.CursedObject import CursedObject
import curses

class Guide(CursedObject):
    """Displays quick shortcuts at the bottom of the screen"""

    def __init__(self, screen):
        self.screen = screen
        self.draw_type = 'draw_keys'

    def draw(self):
        draw_mtd = getattr(self, self.draw_type)
        lines = draw_mtd()

        for i in range(3):
            self.center_text(lines[i], self.height() - (5-i))

    def draw_cmd_line(self):
        first_line = "search: \"artist\", \"album\", \"song\", or \"radio\""
        second_line = "playback: \"play\", \"pause\", \"stop\", \"next\", \"previous\""

    def draw_keys(self):
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
            "  i: Cmd Line "+\
            "  r: Radio     "

        return (first_line, second_line, third_line)
