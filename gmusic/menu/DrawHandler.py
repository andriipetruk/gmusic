from gmusic.menu.CursedObject import CursedObject
from gmusic.menu.CursedMenu import CursedMenu
from gmusic.menu.CursedUI import CursedUI
from gmusic.menu.Guide import Guide
from gmusic.menu.NowPlaying import NowPlaying
import threading

class DrawHandler(CursedObject):
    def __init__(self, state, cache):
        self.state = state
        self.cache = cache

    def launch(self, input_parser):
        self.start()
        self.create_system()
        self.screen.clear()
        self.screen.refresh()
        self.draw()
        self.launch_ui_thread(input_parser)

    def create_system(self):
        '''Builds all of the components and sends them the unified screen'''
        self.now_playing = NowPlaying(self.screen)
        self.menu = CursedMenu(self.screen)
        self.guide = Guide(self.screen)

    def launch_ui_thread(self, parser):
        """Launches a UI thread"""
        cursed_ui = CursedUI(self.screen, parser)
        ui_thread = threading.Thread(target=cursed_ui.__running__)
        ui_thread.start()

    def draw(self):
        self.menu.draw()
        self.now_playing.draw()
        self.guide.draw()
