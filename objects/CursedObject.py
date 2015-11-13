import curses, os, sys, math

class CursedObject(object):
    '''Base object for everything dealing with Curses'''

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

    def __exit__(self):
        curses.endwin()
        os.system('clear')


    ''' I/O '''
    def clear_line(self,row):
        '''Clear a specified row'''
        curr_y, curr_x = self.screen.getyx()
        self.screen.chgat(row,0)
        self.screen.clrtoeol()
        self.screen.chgat(curr_y,curr_x)

    def clear_rows_below(self, row):
        '''Clear from a row to the bottom'''
        curr_y, curr_x = self.screen.getyx()
        self.screen.chgat(row,0)
        self.screen.clrtobot()
        self.screen.chgat(curr_y,curr_x)

    def print_line(self,text,row, column=1,style=curses.A_NORMAL):
        '''Print a line which takes up the whole row'''
        width = self.width()
        text += ' '*int(width-len(text)-column-2)
        self.screen.addstr(row, column, text, style)

    def compress_text(self, text, max_width):
        '''Change a "string that's too long" to "string t...too long" '''
        if max_width < len(text):
            return text[:int(max_width/4)] + "..." + text[int(3*max_width/4):]
        return text

    def center_text(self,text,r,style=curses.A_NORMAL):
        '''Auto-center text in a row; capable of fitting to screen'''

        # Check to make sure it's not too big... if so, replace the middle half with '...'
        width = self.width()
        text = self.compress_text(text, width-4)

        # Center the text
        diff = width - len(text)
        text = ' '*int(math.floor(diff/2)-1) + text
        self.print_line(text,r)


    '''HELPERS'''
    def width(self):
        '''Get the width'''
        ignored, width = self.screen.getmaxyx()
        return width

    def height(self):
        '''Get the height'''
        height, ignored = self.screen.getmaxyx()
        return height

    def height_and_width(self):
        '''Alias for getmaxyx'''
        return self.screen.getmaxyx()
