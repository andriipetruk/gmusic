import curses, os, sys, math

#pylint: disable=no-member
class CursedObject(object):
    '''Base object for everything dealing with Curses'''

    def __init__(self):
        self.screen = None

    def __start__(self):
        '''Start a screen'''
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.start_screen()
        self.start_curses()

    def start_screen(self):
        '''Screen Init'''
        self.screen = curses.initscr()
        self.screen.refresh()
        self.screen.keypad(1)

    def start_curses(self):
        '''Curses Init'''
        curses.noecho()
        curses.cbreak()
        curses.start_color()

    def exit(self):
        """Exits the program"""
        curses.endwin()
        os.system('clear')
        os.system('stty sane')



    def clear_line(self, row):
        '''Clear a specified row'''
        self.run_method_at(row, 0, self.screen.clrtoeol)

    def clear_rows_below(self, row):
        '''Clear from a row to the bottom'''
        self.run_method_at(row, 0, self.screen.clrtobot)

    def print_line(self, text, row, style=curses.A_NORMAL):
        '''Print a line which takes up the whole row'''
        width = self.width()
        text += ' '*int(width-len(text)-4)
        self.screen.addstr(row, 2, text, style)

    def compress_text(self, text, max_width):
        '''Change a "string that's too long" to "string t...too long" '''
        if max_width < len(text):

            return text[:int(3*max_width/4)]+"..."+text[3-int(max_width/4):]
        return text

    def pad_text(self, text, width):
        """Pad text with spaces (if possible)"""
        if len(text) > width:
            return text
        text += ' '*int(width-len(text))
        return text

    def compress_and_pad(self, text, width):
        compressed = self.compress_text(text,width)
        return self.pad_text(compressed,width)


    def center_text(self, text, row):
        '''Auto-center text in a row; capable of fitting to screen'''

        # Check to make sure it's not too big... if so, replace the middle half with '...'
        width = self.width()
        text = self.compress_text(text, width-4)

        # Center the text
        diff = width - len(text)
        text = ' '*int(math.floor(diff/2)-1) + text
        self.print_line(text, row)


    def run_method_at(self, row, column, method):
        '''Assigns the cursor to a position, runs a method, then returns to the original position'''
        curr_y, curr_x = self.screen.getyx()
        self.screen.chgat(row, column)
        method()
        self.screen.chgat(curr_y, curr_x)

    def width(self):
        '''Get the width'''
        return self.screen.getmaxyx()[1]

    def height(self):
        '''Get the height'''
        return self.screen.getmaxyx()[0]

    def height_and_width(self):
        '''Alias for getmaxyx'''
        return self.screen.getmaxyx()
