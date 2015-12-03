from gmusic.menu.CursedObject import CursedObject
from gmusic.menu.Menu import Menu
from gmusic.menu.UI import UI
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
        self.menu = Menu(self.screen)
        self.guide = Guide(self.screen)

    def launch_ui_thread(self, parser):
        """Launches a UI thread"""
        ui = UI(self, parser)
        ui_thread = threading.Thread(target=ui.__running__)
        ui_thread.start()

    def draw(self):
        self.menu.draw()
        self.now_playing.draw()
        self.guide.draw()

    def receive_ui_event(self, event):

        pass
