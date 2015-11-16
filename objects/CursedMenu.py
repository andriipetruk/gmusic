from objects.NowPlaying import NowPlaying
from objects.CursedObject import CursedObject
from objects.CursedUI import CursedUI
import curses, threading

class CursedMenu(CursedObject):
    '''A class which abstracts the horrors of building a curses-based menu system'''

    def __init__(self, content_manager):
        '''Initialization'''
        self.__start__()
        self.cursed_ui = None
        self.options = None

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

    def start(self):
        '''Start up the Menu'''
        self.screen.clear()
        self.screen.refresh()
        self.now_playing.draw(new_track=None)
        self.draw()
        self.is_drawable = True
        self.launch_ui_thread()

    def draw(self):
        '''Draw the menu and lines'''
        self.clear_rows_below(6)
        self.screen.refresh()

        self.print_line(self.content_manager.title, 6, curses.A_BOLD)
        self.print_line(self.content_manager.subtitle, 8, curses.A_BOLD)

        # Display all the menu items, showing the 'pos' item highlighted
        for index in range(len(self.options)):
            textstyle = self.normal
            if index == self.content_manager.selected:
                textstyle = self.highlighted
            self.screen.addstr(9+index, 4, "%d.\t%s" % (index+1, self.options[index]), textstyle)

        self.screen.border(0)
        self.screen.refresh()

    def notify(self, options, page=0):
        """Notification handler; tells everything to redraw"""
        self.adjust_options_for_pages(options, page)
        if not self.content_manager.main_menu:
            self.options.append('Back')
        if self.is_drawable:
            self.now_playing.draw(new_track=None)
            self.draw()
        return self.options

    def adjust_options_for_pages(self, options, page):
        """Figures out how many elements are on a page and gets the appropriate
        ones according to the current page"""
        elements_per_page = self.height()-16
        lower_bound = page*elements_per_page
        upper_bound = (page+1)*elements_per_page
        self.options = options[lower_bound:upper_bound]

    def launch_ui_thread(self):
        """Launches a UI thread"""
        self.cursed_ui = CursedUI(self.screen, self.content_manager)
        ui_thread = threading.Thread(target=self.cursed_ui.__running__)
        ui_thread.start()
