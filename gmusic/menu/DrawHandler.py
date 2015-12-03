from gmusic.menu.NowPlaying import NowPlaying
from gmusic.menu.CursedMenu import CursedMenu
from gmusic.menu.Guide import Guide
from gmusic.menu.CursedObject import CursedObject

class DrawHandler:
    def __init__(CursedObject):
        self.start()

    def create_system(self):
        '''Builds all of the components and sends them the unified screen'''
        self.now_playing = NowPlaying(self.screen)
        self.menu = CursedMenu(self.screen)
        self.guide = Guide(self.screen)
