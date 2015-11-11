from blessed import Terminal
from objects.RequestHandler import RequestHandler
import curses, os, traceback, sys

class CursedMenu(object):
    '''A class which abstracts the horrors of building a curses-based menu system'''

    def __init__(self, content_manager, request_handler):
        '''Initialization'''
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.terminal = Terminal()
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)

        # Highlighted and Normal line definitions
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlighted = curses.color_pair(1)
        self.normal = curses.A_NORMAL

        # Attached objects
        self.content_manager = content_manager
        self.request_handler = request_handler


    def show(self):
        self.set_parameters()
        self.draw_menu()


    def set_parameters(self):
        '''Draws a menu with the given parameters'''
        if self.content_manager.search_menu:
            options = [a['title'] for a in self.content_manager.search_results]
            if len(options) > 50:
                options = options[:50]
            self.set_options(options)
            self.title = self.content_manager.title
            self.subtitle = self.content_manager.subtitle
        else:
            self.set_options(self.content_manager.get_most_recent_searches())
            self.title = "Main Menu"
            self.subtitle = "Options"
        self.selected = 0


    def set_options(self, options):
        '''Validates that the last option is "Exit"'''
        if (options[-1] is not 'Exit' and not self.content_manager.search_menu):
            options.append('Exit')
        if (options[-1] is not 'Back' and self.content_manager.search_menu):
            options.append('Back')
        self.options = options


    def draw_menu(self):
        '''Actually draws the menu and handles branching'''
        request = ""
        try:
            while request is not "Exit":
                self.draw()
                request = self.get_user_input()
                self.handle_request(request)
            self.__exit__()

        # Also calls __exit__, but adds traceback after
        except Exception as exception:
            self.__exit__()
            traceback.print_exc()


    def center_text(self,text,r,style=curses.A_NORMAL):
        self.screen.addstr(r,int((self.terminal.width-len(text))/2), text, style)

    def draw_now_playing(self):
        if self.content_manager.now_playing_track is not "":
            self.center_text(self.content_manager.now_playing_track['title'], 2, curses.A_BOLD)
            self.center_text(self.content_manager.now_playing_track['album'], 3, self.normal)
            self.center_text(self.content_manager.now_playing_track['artist'], 4, self.normal)
            return
        self.center_text("Google Music Terminal",3,curses.A_BOLD)

    def draw(self):
        '''Draw the menu and lines'''
        self.screen.clear()
        self.screen.border(0)

        self.draw_now_playing()
        self.screen.addstr(6,2, self.title, curses.A_STANDOUT) # Title for this menu
        self.screen.addstr(8,2, self.subtitle, curses.A_BOLD) #Subtitle for this menu

        # Display all the menu items, showing the 'pos' item highlighted
        for index in range(len(self.options)):
            textstyle = self.normal
            if index == self.selected:
                textstyle = self.highlighted
            self.screen.addstr(9+index,4, "%d - %s" % (index+1, self.options[index]), textstyle)

        self.screen.refresh()


    def get_user_input(self):
        '''Gets the user's input and acts appropriately'''
        user_in = self.screen.getch() # Gets user input

        '''Enter and Exit Keys are special cases'''
        if user_in == 10:
            if self.selected == (len(self.options)-1):
                return self.options[-1]
            if self.content_manager.search_menu:
                return 'play {0}'.format(self.selected)
            return self.content_manager.most_recent_searches[self.selected]
        if user_in == 27:
            self.__exit__()
            return

        # This is a number; check to see if we can set it
        if user_in >= ord('1') and user_in <= ord(str(min(9,len(self.options)+1))):
            self.selected = user_in - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
            return

        if user_in == ord(' '):
            return 'pause'

        if user_in == ord('i'):
            return self.handle_text_entry()

        # Increment or Decrement
        if user_in == curses.KEY_DOWN: # down arrow
            self.selected += 1
        if user_in == curses.KEY_UP: # up arrow
            self.selected -=1
        self.selected = self.selected % len(self.options)
        return


    def handle_text_entry(self):
        curses.echo()
        self.screen.addstr(self.terminal.height-2, 2, "> ")
        self.screen.refresh()
        rin =  self.screen.getstr(self.terminal.height-2, 4, self.terminal.width-4)
        curses.noecho()
        return rin


    def handle_request(self, request):
        '''This is where you do things with the request'''
        if request is None: return

        self.request_handler.parse(request)
        if (('artist' in request or 'album' in request or 'song' in request) and request not in self.content_manager.most_recent_searches):
            self.content_manager.most_recent_searches.append(request)
        self.set_parameters()


    def __exit__(self):
        curses.endwin()
        os.system('clear')
