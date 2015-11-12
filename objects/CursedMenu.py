from blessed import Terminal
from objects.RequestHandler import RequestHandler
from objects.NowPlaying import NowPlaying
from objects.CursedObject import CursedObject
from objects.CursedUI import CursedUI
import curses, traceback, sys, threading, time

class CursedMenu(CursedObject):
    '''A class which abstracts the horrors of building a curses-based menu system'''

    def __init__(self, content_manager):
        '''Initialization'''
        self.__start__()
        self.terminal = Terminal()

        # Highlighted and Normal line definitions
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlighted = curses.color_pair(1)
        self.normal = curses.A_NORMAL
        self.is_drawable = False

        # Attached objects
        self.content_manager = content_manager
        content_manager.attach(self)
        self.now_playing = NowPlaying(self.screen)
        content_manager.attach_to_streamer(self.now_playing)

    def show(self):
        self.launch_ui_thread()
        self.screen.clear()
        self.screen.refresh()
        self.now_playing.draw()
        self.draw()
        self.is_drawable = True

    def draw(self):
        '''Draw the menu and lines'''
        self.clear_rows_below(6)
        self.screen.refresh()

        self.screen.addstr(6,2, self.content_manager.title, curses.A_STANDOUT) # Title for this menu
        self.screen.addstr(8,2, self.content_manager.subtitle, curses.A_BOLD) #Subtitle for this menu

        # Display all the menu items, showing the 'pos' item highlighted
        for index in range(len(self.options)):
            textstyle = self.normal
            if index == self.content_manager.selected:
                textstyle = self.highlighted
            self.screen.addstr(9+index,4, "%d - %s" % (index+1, self.options[index]), textstyle)

        self.screen.border(0)
        self.screen.refresh()

    def notify(self, options, page=0):
        elements_per_page = self.height()-16
        self.options = options[page*elements_per_page:(page+1)*elements_per_page]
        if not self.content_manager.main_menu:
            self.options.append('Back')
        if self.is_drawable:
            self.now_playing.draw()
            self.draw()
        return self.options

    def launch_ui_thread(self):
        self.ui = CursedUI(self.screen,self.content_manager)
        ui_thread = threading.Thread(target=self.ui.__running__)
        ui_thread.start()
