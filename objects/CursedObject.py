import curses, os, sys, math

class CursedObject(object):
    '''Base object for everything dealing with Curses'''

    def __start__(self):
        '''Start a screen'''
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.screen = curses.initscr()
        self.screen.refresh()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)
        os.system('setterm -cursor off')

    def __exit__(self):
        curses.endwin()
        os.system('clear')
        os.system('setterm -cursor on')


    def clear_line(self,row):
        '''Clear a specified row'''
        curr_y, curr_x = self.screen.getyx()
        self.screen.chgat(row,0)
        self.screen.clrtoeol()
        self.screen.chgat(curr_y,curr_x)

    def clear_rows_below(self, row):
        curr_y, curr_x = self.screen.getyx()
        self.screen.chgat(row,0)
        self.screen.clrtobot()
        self.screen.chgat(curr_y,curr_x)

    def center_text(self,text,r,style=curses.A_NORMAL):
        '''Auto-center text in a row; capable of fitting to screen'''
        # Check to make sure it's not too big... if so, replace the middle half with '...'
        height, width = self.screen.getmaxyx()
        if (width-4) < len(text):
            text = text[:int(width/4)] + "..." + text[int(3*width/4):]

        diff = width - len(text)
        text = ' '*int(math.floor(diff/2)-1) + text + ' '*int(math.ceil(diff/2)-1)

        # Add the string, then go back
        self.screen.addstr(r,1, text, style)



    '''HELPERS'''
    def width(self):
        ignored, width = self.screen.getmaxyx()
        return width

    def height(self):
        height, ignored = self.screen.getmaxyx()
        return height
