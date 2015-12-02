from gmusic.menu.CursedObject import CursedObject
import curses

class NowPlaying(CursedObject):
    """Now Playing banner written for Curses"""

    def __init__(self, screen):
        self.track = {"eos": True}
        self.screen = screen

    def check_track(self, new_track):
        """
        Check to see if the new track is actually new, then figures out
        what to do if it is new
        """
        if new_track is not None:
            self.track = new_track
        if 'eos' in self.track:
            self.draw_no_track()
        else:
            self.draw_track_details()
        self.screen.refresh()

    def draw_no_track(self):
        """Draws a blank banner if there's not a song playing"""
        self.center_text('  ', 2)
        self.center_text("Google Music Terminal", 3)
        self.center_text('  ', 4)

    def draw_track_details(self):
        """Draws a banner for the current track if it is playing"""
        self.center_text(self.track['title'], 2)
        self.center_text(self.track['album'], 3)
        self.center_text(self.track['artist'], 4)

    def draw(self, new_track):
        """Master draw method, checks the new_track to see what to draw"""
        self.check_track(new_track)
