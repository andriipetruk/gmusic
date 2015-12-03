from gmusic.content.ContentHandler import ContentHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.core.Cache import Cache
from gmusic.core.State import State
from gmusic.core.CommandParser import CommandParser
from gmusic.core.UIParser import UIParser
from gmusic.frontend.DrawHandler import DrawHandler
from gmusic.frontend.UI import UI
import sys

class Core:
    def __init__(self):
        self.cache = Cache()
        self.state = State()
        self.draw_handler = DrawHandler(self.cache, self.state)

    def build_parsers(self):
        content_handler = ContentHandler()
        content_handler.launch()

        # Player Controller
        player_controller = PlayerController(content_handler)
        player_controller.attachments.append(self)
        player_controller.start()

        cmd_parser = CommandParser(self, content_handler, player_controller)
        ui_parser = UIParser(event_handler=self, command_parser=cmd_parser)

        return (cmd_parser, ui_parser)

    def start(self):
        cmd_parser, ui_parser = self.build_parsers()
        self.draw_handler.launch(cmd_parser, ui_parser)

    def handle_event(self, event, args=None):
        if 'CHANGE' in event:
            self.draw_handler.redraw()

        if 'PLAY' in event:
            self.draw_handler.banner_update(args)

        if 'STOP' in event:
            self.draw_handler.banner_update(None)

        if 'EXIT' in event:
            self.draw_handler.exit()
            sys.exit(1)
