from gmusic.frontend.CursedObject import CursedObject
from gmusic.core.CommandParser import CommandParser
from gmusic.core.EventHandler import EventHandler
from gmusic.core.UIParser import UIParser
import curses

class UI(CursedObject, EventHandler):
    """Asynchronous. Handles input from the user"""

    def __init__(self, draw_handler, cmd_parser, ui_parser):
        CursedObject.__init__(self)
        EventHandler.__init__(self)
        self.attachments.append(draw_handler)
        self.screen = draw_handler.screen
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
            self.notify_attachments('PageUpdate')
            return

        # Otherwise it goes off to the UI Parser
        self.ui_parser.parse(user_input)

    def handle_text_entry(self):
        """Handles full-text entry, instead of keypresses"""
        curses.echo()
        height, width = self.screen.getmaxyx()

        request = self.draw_cli_prompt(height, width)

        # Push it to cmd_parser
        curses.noecho()
        self.cmd_parser.parse(request)

    def draw_cli_prompt(self, height, width):
        win = curses.newwin(14, 60, height-20, int(width*0.5)-30)
        win.box()
        win_h, win_w = win.getmaxyx()
        win.addstr(0, 2, 'Commands', curses.A_BOLD)
        win.addstr(1, 2, '"album ____"       Search for Albums', curses.A_DIM)
        win.addstr(2, 2, '"artist ____"      Search for Artists', curses.A_DIM)
        win.addstr(3, 2, '"playlist ____"    Search for Playlists', curses.A_DIM)
        win.addstr(4, 2, '"radio ____"       Search for Radios', curses.A_DIM)
        win.addstr(5, 2, '"song ____"        Search for Songs', curses.A_DIM)
        win.addstr(6, 2, '"play"/"pause"     General Playback', curses.A_DIM)
        win.addstr(7, 2, '"next"/"previous"  Play Next or Previous', curses.A_DIM)
        win.addstr(8, 2, '"random"           Toggle Shuffle', curses.A_DIM)
        win.addstr(9, 2, '"back"             Back to Main Menu', curses.A_DIM)
        win.addstr(10, 2, '"exit"             Exit the program', curses.A_DIM)
        win.addstr(win_h-2, 2, "> ")
        self.screen.refresh()
        win.refresh()
        return win.getstr(win_h-2, 4, win_w-4)
