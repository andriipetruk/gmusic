from gmusic.content.ContentHandler import ContentHandler
from gmusic.player.PlayerController import PlayerController
from gmusic.input.InputParser import InputParser

class Interface(object):
    """This is the command line interface. It handles
    all user input and sends to the processor as necessary"""

    def __init__(self):
        """Initialization"""
        self.content_handler = ContentHandler()
        self.player_controller = PlayerController(self.content_handler)
        self.parser = InputParser(self.content_handler, self.player_controller)

    def start(self):
        """Our default running loop which governs the UI"""
        self.content_handler.launch()
        print('Loaded!')
        self.do_interface_loop()

    def do_interface_loop(self):
        cmd = ''
        while cmd != '/exit':
            cmd = raw_input('')
            self.parser.parse(cmd)

    #    self.display.start()
