from gmusic.content.ContentHandler import ContentHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.core.Cache import Cache
from gmusic.core.State import State
from gmusic.core.CommandParser import CommandParser
from gmusic.frontend.DrawHandler import DrawHandler
from gmusic.frontend.UI import UI

class Core:
    def __init__(self):
        self.cache = Cache()
        self.state = State()
        self.build_parser()
        self.draw_handler = DrawHandler(self.cache, self.state)

    def build_parser(self):
        # Content Handler
        content_handler = ContentHandler()
        content_handler.launch()

        # Player Controller
        player_controller = PlayerController(content_handler)
        player_controller.attachments.append(self)
        player_controller.start()
        return InputParser(content_handler, player_controller)

    def start(self):
        self.draw_handler.launch(parser)

    def handle_event(self, event):
        pass
