from gmusic.content.ContentHandler import ContentHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.core.CommandParser import CommandParser
from gmusic.core.MasterEventHandler import MasterEventHandler
from gmusic.core.UIParser import UIParser
from gmusic.frontend.UI import UI

class Core:
    def start(self):
        '''Launch all elements'''
        # Build and launch player and content entry points
        meh = MasterEventHandler()
        content_handler = ContentHandler()
        content_handler.attachments.append(meh)
        content_handler.launch()

        player_controller = PlayerController(content_handler)
        player_controller.attachments.append(meh)
        player_controller.start()

        # Build the parsers
        cmd_parser = CommandParser(meh, content_handler, player_controller)
        ui_parser = UIParser(event_handler=meh, command_parser=cmd_parser)
        meh.draw_handler.launch(cmd_parser, ui_parser)
