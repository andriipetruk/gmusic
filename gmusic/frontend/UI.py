from gmusic.frontend.CursedObject import CursedObject
from gmusic.core.CommandParser import CommandParser
from gmusic.core.UIParser import UIParser
import curses

class UI(CursedObject):
    """Asynchronous. Handles input from the user"""

    def __init__(self, draw_handler, input_parser):
        CursedObject.__init__(self)
        self.screen = draw_handler.screen
        self.attachments = [draw_handler]
        self.input_parser = input_parser

    def __running__(self):
        """Runs an infinite loop so long as the request is not an exit cmd"""
        request = ""
        while request != 'exit':
            request = self.get_user_input()
            self.handle_request(request)

        self.content_manager.exit()


    def get_user_input(self):
        '''Gets the user's input and acts appropriately'''

        print('getting input')
        user_in = self.screen.getch() # Gets user input

        # Enter Key
        if user_in == 10:
            return self.content_manager.handle_execute().lower()

        # Escape
        if user_in == 27:
            self.content_manager.exit()
            return 'exit'

        # Spacebar
        if user_in == ord(' '):
            return 'pause'

        # i (text entry)
        if user_in == ord('i') or user_in == ord('I'):
            result = self.handle_text_entry()
            #self.content_manager.menu.draw()
            return result

        # n (next)
        if user_in == ord('n'):
            return "next"


        # Page Increment/Decrement
        if user_in == ord('['):
            self.content_manager.change_page(-1)
            return
        if user_in == ord(']'):
            self.content_manager.change_page(1)
            return


        # Increment or Decrement
        if user_in == curses.KEY_NPAGE:
            self.content_manager.adjust_selection(10)
        if user_in == curses.KEY_PPAGE:
            self.content_manager.adjust_selection(-10)
        if user_in == curses.KEY_DOWN: # down arrow
            self.content_manager.adjust_selection(1)
        if user_in == curses.KEY_UP: # up arrow
            self.content_manager.adjust_selection(-1)
        return


    def handle_text_entry(self):
        """Handles full-text entry, instead of keypresses"""
        curses.echo()
        height, width = self.screen.getmaxyx()
        self.screen.addstr(height-2, 2, "> ")
        self.screen.refresh()
        rin = self.screen.getstr(height-2, 4, width-4)
        curses.noecho()
        return rin


    def handle_request(self, request):
        '''This is where you do things with the request'''
        if request is None:
            return

        self.input_parser.parse(request)
