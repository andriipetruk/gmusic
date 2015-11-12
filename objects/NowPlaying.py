from objects.CursedObject import CursedObject
import time, curses

class NowPlaying(CursedObject):
    def __init__(self, screen):
        self.track = {"eos": True}
        self.screen = screen

    def check_track(self, new_track):
        if len(new_track) > 0:
            self.track = new_track
        curr_y, curr_x = self.screen.getyx()
        if 'eos' in self.track:
            self.draw_no_track()
        else:
            self.draw_track_details()
        self.screen.refresh()

    def draw_no_track(self):
        self.center_text('  ',2,curses.A_NORMAL)
        self.center_text("Google Music Terminal",3,curses.A_BOLD)
        self.center_text('  ',4,curses.A_NORMAL)

    def draw_track_details(self):
        self.center_text(self.track['title'], 2, curses.A_BOLD)
        self.center_text(self.track['album'], 3, curses.A_NORMAL)
        self.center_text(self.track['artist'], 4, curses.A_NORMAL)

    def draw(self, new_track=[]):
        self.check_track(new_track)
