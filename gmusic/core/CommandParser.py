from gmusic.core.CommandHandler import CommandHandler

class CommandParser(object):
    """Class which is responsible for decoding user input"""

    def __init__(self, event_handler, content_handler, player_controller):
        self.handler = CommandHandler(event_handler, content_handler, player_controller)

    def parse(self, line):
        '''Master method; figures out what was typed by the user'''
        if line is '':
            return

        data = line.split(' ', 1)

        # Default content to empty string
        if len(data) == 1:
            data.append("")
        self.handle(data)

    def handle(self, data):
        """Get the correct method and invoke it"""
        method_type = 'typed_{0}'.format(data[0].lower())
        if hasattr(self.handler, method_type):
            method = getattr(self.handler, method_type)
            method(data[1])
