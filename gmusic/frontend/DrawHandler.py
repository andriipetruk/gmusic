from gmusic.frontend.CursedObject import CursedObject
from gmusic.frontend.Menu import Menu
from gmusic.frontend.UI import UI
from gmusic.frontend.Guide import Guide
from gmusic.frontend.Banner import Banner
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
        self.banner = Banner(self.screen)
        self.menu = Menu(self.screen)
        self.guide = Guide(self.screen)

    def launch_ui_thread(self, parser):
        """Launches a UI thread"""
        ui = UI(self, parser)
        ui_thread = threading.Thread(target=ui.__running__)
        ui_thread.start()

    def draw(self):
        self.menu.draw()
        self.banner.draw()
        self.guide.draw()

    def receive_ui_event(self, event):

        pass
