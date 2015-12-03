from gmusic.frontend.CursedObject import CursedObject
from gmusic.core.CommandParser import CommandParser
from gmusic.core.UIParser import UIParser
import curses

class UI(CursedObject):
    """Asynchronous. Handles input from the user"""

    def __init__(self, draw_handler, cmd_parser, ui_parser):
        CursedObject.__init__(self)
        self.screen = draw_handler.screen
        self.attachments = [draw_handler]
        self.cmd_parser = cmd_parser
        self.ui_parser = ui_parser

    def __running__(self):
        """Runs an infinite loop so long as the request is not an exit cmd"""
        request = ""
        while request != 'exit':
            self.get_user_input()
        self.content_manager.exit()

    def get_user_input(self):
        '''Get the character pressed by the user, then send it'''
        user_input = self.screen.getch()

        # Text Entry must occur here, in curses land
        if user_input == ord('i') or user_input == ord('I'):
            result = self.handle_text_entry()
            self.notify_attachments('CLEAR TEXT ENTRY')
            return

        # Otherwise it goes off to the UI Parser
        self.ui_parser.parse(user_input)

    def handle_text_entry(self):
        """Handles full-text entry, instead of keypresses"""
        curses.echo()
        height, width = self.screen.getmaxyx()

        # Start the entry
        self.screen.addstr(height-2, 2, "> ")
        self.screen.refresh()
        request = self.screen.getstr(height-2, 4, width-4)
        curses.noecho()
        # Push it to cmd_parser
        self.cmd_parser.parse(request)

    def notify_attachments(self, event, args=None):
        for attachment in self.attachments:
            attachment.handle_event(event)
