from gmusic.curses.NowPlaying import NowPlaying
from gmusic.curses.CursedObject import CursedObject
from gmusic.curses.CursedUI import CursedUI
from gmusic.curses.Guide import Guide
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
        self.now_playing = NowPlaying(self.screen)
        self.guide = Guide(self.screen)
        content_manager.attach(self)
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
        self.guide.draw()

        self.screen.border(0)
        self.screen.refresh()

    def notify(self, options, page=0):
        """Notification handler; tells everything to redraw"""
        page_options = self.get_page_options(options, page)
        self.options = self.adjust_titles_for_menu_type(page_options, page)

        if not self.content_manager.main_menu:
            page_options.append('Back')
            self.options.append('Back')

        if self.is_drawable:
            self.now_playing.draw(new_track=None)
            self.draw()
        return page_options

    def get_page_options(self,options,page):
        elements_per_page = self.height()-16
        lower_bound = page*elements_per_page
        upper_bound = (page+1)*elements_per_page
        return options[lower_bound:upper_bound]

    def adjust_titles_for_menu_type(self, options, page):
        """Figures out how many elements are on a page and gets the appropriate
        ones according to the current page"""
        if self.content_manager.main_menu:
            return options
        return [self.format_title(a) for a in options]

    def format_title(self, track):
        """Formats a track for display in menu"""
        song_width = int(self.width()/2)-4
        album_width = int(self.width()/3)-4
        title = self.compress_and_pad(track['title'], width=song_width)
        album = self.compress_and_pad(track['album'], width=album_width)
        return title + " " + album



    def launch_ui_thread(self):
        """Launches a UI thread"""
        self.cursed_ui = CursedUI(self.screen, self.content_manager)
        ui_thread = threading.Thread(target=self.cursed_ui.__running__)
        ui_thread.start()
