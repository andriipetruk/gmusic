from gmusic.frontend.CursedObject import CursedObject
from gmusic.core.CommandParser import CommandParser
from gmusic.core.EventHandler import EventHandler
from gmusic.core.UIParser import UIParser
import curses
import collections

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

        # TODO: figure out how to have the UI listen fo the escape key
        # elif user_input == 27: # 27 is escape
        #     del self.cli_prompt
        #     self.screen.refresh()
        #     return

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
        indentation = 2
        screen_padding = 20
        text_padding = 12

        # Content
        help_options = collections.OrderedDict()

        help_options['album'] =     '> album title     Search for Albums'
        help_options['artist'] =    '> artist name     Search for Artists'
        help_options['playlist'] =  '> playlist name   Search for Playlists'
        help_options['radio'] =     '> radio name      Search for Radios'
        help_options['song'] =      '> song title      Search for Songs'
        help_options['play'] =      '> play            Begins Playback'
        help_options['pause'] =     '> pause           Pauses Playback'
        help_options['next'] =      '> next            Play Next'
        help_options['previous'] =  '> previous        Play Previous'
        help_options['random'] =    '> random          Toggle Shuffle'
        help_options['back'] =      '> back            Returns to the previous page'
        help_options['main'] =      '> main            Back to Main Menu'
        help_options['exit'] =      '> exit            Exit the program'

        # Examples for the above (only used if the window is wide enough)
        examples = {
            'album': '\t\te.g.:  > album Discovery',
            'artist': '\t\te.g.:  > artist Daft Punk',
            # the playlist is a long word
            # and messes up the tabbing
            # TODO: see if there is a curses table implementation
            # where we could just draw to table cells
            'playlist': '\te.g.:  > playlist Eletro-Ambient',
            'radio': '\t\te.g.:  > radio Armin',
            'song': '\t\te.g.:  > song aerodynamic'
        }

        # calculate the longest line of text
        # this will be used to compare with the window width to see
        # if we even can add the examples
        longest_core_option_length = len(max(help_options.values(), key=len))
        longest_example_length = len(max(examples.values(), key=len))
        longest_help_text = longest_core_option_length + longest_example_length

        # Height is based off the content of the cli
        # + a blank line
        # + a line for input
        # + the top and bottom borders (2)
        window_height = len(help_options) + 1 + 1 + 2
        window_width = width - (screen_padding * 2)

        # determine if the window width should be shorter
        if window_width < (longest_help_text + screen_padding * 2):
            # reduce width to fit just the help
            window_width = longest_core_option_length + text_padding
        else:
            # window is plenty wide, add the examples
            window_width = longest_help_text + text_padding
            for command, text in examples.items():
                help_options[command] = help_options[command] + text

        # Height of this window with some padding underneath
        begin_y = height - (window_height + 4)
        # half the width of the screen minus half the width of the window
        begin_x = int(width * 0.5) - (window_width / 2)

        # Now that we have all our parameters for constraining the window,
        # create the window
        self.cli_prompt = win = curses.newwin(window_height, window_width, begin_y, begin_x)

        win.box()
        win_h, win_w = win.getmaxyx()

        # The first line of text will be at this height from the top of the window
        line_index = 1
        last_line_index = window_height - 2
        # Title
        win.addstr(0, indentation, 'Commands', curses.A_BOLD)

        # Add the text to the window
        for command, text in help_options.items():
            win.addstr(line_index, indentation, text, curses.A_DIM)
            line_index += 1

        #win.addstr(14, 2, 'ESC will close this modal', curses.A_DIM)
        win.addstr(line_index, indentation, '', curses.A_DIM)
        win.addstr(last_line_index, indentation, "> ")

        # draw everything
        self.screen.leaveok(1)
        self.screen.refresh()
        win.refresh()

        # listen for commands
        return win.getstr(last_line_index, indentation * 2, win_w-(indentation * 2))
