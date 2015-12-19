from gmusic.content.ContentHandler import ContentHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.core.CommandProcessor import CommandProcessor
from gmusic.core.MasterEventHandler import MasterEventHandler
from gmusic.core.UIParser import UIParser
from gmusic.frontend.UI import UI

class Core:
    def start(self):
        '''Launch all elements'''
        # Build and launch player and content entry points
        master = MasterEventHandler()
        content_handler = ContentHandler()
        content_handler.attachments.append(master)
        content_handler.launch()

        player_controller = PlayerController(content_handler)
        player_controller.attachments.append(master)
        player_controller.start()

        # Build the parsers
        cmd_parser = CommandProcessor(master, content_handler, player_controller)
        ui_parser = UIParser(event_handler=master, command_parser=cmd_parser)
        master.draw_handler.launch(cmd_parser, ui_parser)
