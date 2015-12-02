from gmusic.menu.NowPlaying import NowPlaying
from gmusic.menu.CursedMenu import CursedMenu
from gmusic.menu.Guide import Guide

class DrawHandler:
    def __init__(self):
        self.now_playing = NowPlaying()
        self.menu = CursedMenu()
        self.guide = Guide()

    def create_system(self):
        pass
