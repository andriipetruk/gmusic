from objects.StreamerWrapper import StreamerWrapper
import math

class ContentManager(object):
    """Main class for controlling what content is available to Gstreamer"""

    def __init__(self):
        self.songs = []
        self.radios = []
        self.search_results = []
        self.most_recent_searches = []
        self.title = ''
        self.subtitle = ''
        self.main_menu = True
        self.page = 0
        self.selected = 0
        self.streamer = StreamerWrapper()
        self.full_options = None
        self.page_options = None

    def load(self):
        """Load Songs, Stations, and Playlists"""
        print "Logged into Google Music. Now loading songs and radios."
        self.set_menu_options()
        self.streamer.run()
        self.songs = self.streamer.client.get_all_songs()
        self.radios = self.streamer.client.get_all_stations()

    def search_songs(self, artist="", album="", song=""):
        """Search for songs matching certain parameters"""
        search_results = [s for s in self.songs \
            if album.lower() in s['album'].lower() \
            and artist.lower() in s['artist'].lower() \
            and song.lower() in s['title'].lower()]

        # Check to see if we should assign results to current state
        if len(search_results) > 0:
            self.assign_search_results(artist+album+song, search_results)

    def assign_search_results(self, search_parameters, search_results):
        """Assigns state-based parameters according to search results"""
        self.title = search_parameters
        self.subtitle = "Search Results"
        self.main_menu = False
        self.search_results = search_results
        self.set_menu_options()


    def get_most_recent_searches(self):
        """Formats 'Most Recent Searches' for main menu"""
        return self.most_recent_searches + ['Options', 'Exit']

    def play_track(self, num):
        """Play a track from the search results"""
        return self.search_results[num]

    def queue(self, track_index):
        """Queue a set of songs for playback"""
        queue = []
        if track_index < len(self.search_results):
            queue += self.search_results[track_index+1:]
        if track_index > 0:
            queue += self.search_results[:track_index-1]

        self.streamer.queue = queue



    def set_menu_options(self):
        '''Draws a menu with the given parameters'''
        if self.main_menu:
            self.selected = 0
            self.full_options = self.get_most_recent_searches()
            self.title = "Main Menu"
            self.subtitle = "Options"
        else:
            self.full_options = [a['title'] for a in self.search_results]

        # Notify the menu (if it exists)
        if hasattr(self, 'menu'):
            self.page_options = self.menu.notify(self.full_options)


    def get_page_number(self):
        """Returns a string formatted like '(Page 2 or 3)'"""
        num_pages = int(math.ceil(len(self.full_options) / len(self.page_options)))
        if num_pages > 1:
            return " (Page {0} of {1})".format(self.page, num_pages)
        return ""


    def back_to_main(self):
        """Returns to main menu"""
        self.main_menu = True
        self.set_menu_options()

    def change_page(self, val):
        """Changes the page by <val>"""
        num_pages = int(math.ceil(len(self.full_options) / len(self.page_options)))
        self.page = min(max(0, self.page+val), num_pages)

        # Notify the menu (if it exists)
        if hasattr(self, 'menu'):
            self.page_options = self.menu.notify(self.full_options, self.page)


    def adjust_selection(self, val):
        """Adjusts the position of the selection cursor in the menu"""
        self.selected += val
        if self.selected > len(self.page_options):
            self.change_page(1)
        if self.selected < 0:
            self.change_page(-1)
        self.selected = self.selected % len(self.page_options)

        # Notify the menu (if it exists)
        if hasattr(self, 'menu'):
            self.menu.draw()


    def handle_execute(self):
        """Runs whenever the Enter key is called (execute command)"""
        if self.selected == len(self.page_options)-1:
            self.page = 0
            return self.page_options[-1]
        if self.main_menu:
            return self.most_recent_searches[self.selected]
        return 'play {0}'.format(self.selected + (len(self.page_options)*self.page))


    def attach_to_streamer(self, now_playing=None):
        """Allows objects to attach to this object's streamer"""
        self.streamer.attach(now_playing)

    def attach(self, menu=None):
        """Allows objects to attach to this object"""
        if menu is not None:
            self.menu = menu

    def exit(self):
        """Calls on the menu to exit the application"""
        self.menu.exit()
