from gmusic.core.UIHandler import UIHandler

class UIParser(object):
    def __init__(self, event_handler, command_parser):
        self.handler = UIHandler(event_handler, command_parser)

    def parse(self, user_input):
        self.handler.handle(user_input)
