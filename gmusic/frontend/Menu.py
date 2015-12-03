from gmusic.frontend.CursedObject import CursedObject
import curses, threading

class Menu(CursedObject):
    '''A class which abstracts the horrors of building a curses-based menu system'''

    def __init__(self, screen):
        '''Initialization'''
        self.screen = screen
        self.options = None

        # Highlighted and Normal line definitions
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlighted = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def draw(self, selected):
        '''Draw the menu and lines'''
        self.clear_rows_below(6)
        self.screen.refresh()

        self.print_line(self.title, 6, curses.A_BOLD)
        self.print_line(self.subtitle, 8, curses.A_BOLD)

        width = self.width()
        max_elements = self.height() - 18

        # Display all the menu items, showing the 'pos' item highlighted
        for index in range(min(max_elements, len(self.options))):
            textstyle = self.normal
            if index == selected:
                textstyle = self.highlighted

            # Use 0 index here, as the tuple pattern is (DISPLAY_STRING, id)
            option = self.compress_text(self.options[index][0], width-4)
            self.screen.addstr(9+index, 4, "%d.\t%s" % (index+1, option), textstyle)

        self.screen.border(0)
        self.screen.refresh()

    def format_title(self, track):
        """Formats a track for display in menu"""
        song_width = int(self.width()/2)-4
        album_width = int(self.width()/3)-4
        title = self.compress_and_pad(track['title'], width=song_width)
        album = self.compress_and_pad(track['album'], width=album_width)
        return title + " " + album
