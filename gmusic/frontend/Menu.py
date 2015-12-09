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
        start_row = 7

        self.clear_rows_below(start_row)
        self.screen.refresh()

        self.print_line(self.title, start_row, curses.A_BOLD)
        self.print_line(self.subtitle, start_row + 2, curses.A_BOLD)

        self.current_width = self.width()

        # Display all the menu items, showing the 'pos' item highlighted
        for index in range(len(self.options)):
            textstyle = self.normal
            if index == selected:
                textstyle = self.highlighted

            # Use 0 index here, as the tuple pattern is (DISPLAY_STRING, id)
            option = self.format_element(self.options[index])
            self.screen.addstr(start_row+index+3, 4, "%d.\t%s" % (index+1, option), textstyle)

        self.screen.border(0)
        self.screen.refresh()

    def format_element(self, menu_element):
        """Formats a track for display in menu"""
        # Use current width because it's already in mem
        if menu_element.alt is None:
            return self.compress_and_pad(menu_element.main, width=self.current_width-8)

        # if alt is nt none
        main_width = int(self.current_width*2/3)-8
        alt_width = int(self.current_width/3)-6
        main = self.compress_and_pad(menu_element.main, width=main_width)
        alt = self.compress_and_pad(menu_element.alt, width=alt_width)
        return main + " " + alt
