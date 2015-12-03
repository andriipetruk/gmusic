from gmusic.menu.MenuCache import MenuCache
from gmusic.menu.MenuState import MenuState
from gmusic.menu.DrawHandler import DrawHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.content.ContentHandler import ContentHandler
from gmusic.input.InputParser import InputParser
from gmusic.menu.CursedUI import CursedUI
import threading

class CursedCore:
    def __init__(self):
        self.cache = MenuCache()
        self.state = MenuState()
        self.draw_handler = DrawHandler()

        # Parser
        content_handler = ContentHandler()
        content_handler.launch()
        player_controller = PlayerController(content_handler)
        player_controller.attachments.append(self)
        player_controller.start()
        self.input_parser = InputParser(content_handler, player_controller)

    def start(self):
        self.launch_ui_thread()

    def handle_event(self, event):
        pass

    def launch_ui_thread(self):
        """Launches a UI thread"""
        query = ""
        while query != 'exit':
            query = raw_input('> ')
            self.input_parser.parse(query)
        #cursed_ui = CursedUI(self.input_parser)
        #ui_thread = threading.Thread(target=cursed_ui.__running__)
        #ui_thread.start()
