from objects.Streamer import Streamer
import math

class ContentManager(object):

    def __init__(self):
        self.songs = []
        self.radios = []
        self.search_results =[]
        self.most_recent_searches = []
        self.title = ''
        self.subtitle = ''
        self.main_menu = True
        self.page = 0
        self.selected = 0
        self.streamer = Streamer()

    def load(self):
        print "Logged into Google Music. Now loading songs and radios."
        self.set_menu_options()
        self.streamer.run()
        self.songs = self.streamer.client.get_all_songs()
        self.radios = self.streamer.client.get_all_stations()

    def search_songs(self,artist="",album="",song=""):
        search_results = [s for s in self.songs if (album.lower() in s['album'].lower() and artist.lower() in s['artist'].lower() and song.lower() in s['title'].lower())]
        if len(search_results) > 0:
            self.title = artist+album+song
            self.subtitle = "Search Results"
            self.main_menu = False
            self.search_results = search_results
            self.set_menu_options(self.search_results)


    def get_most_recent_searches(self):
        return self.most_recent_searches + ['Options', 'Exit']

    def play_track(self, num):
        track = self.search_results[num]
        return track

    def queue(self, track_index):
        queue = []
        if track_index < len(self.search_results):
            queue += self.search_results[track_index+1:]
        if track_index > 0:
             queue += self.search_results[:track_index-1]

        self.streamer.queue = queue


    '''UI Notifications'''
    def set_menu_options(self, opts=[]):
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
        num_pages = int(math.ceil(len(self.full_options) / len(self.page_options)))
        if num_pages > 1:
            return " (Page {0} of {1})".format(self.page,num_pages)
        return ""


    def back_to_main(self):
        self.main_menu = True
        self.set_menu_options()

    def change_page(self, val):
        num_pages = int(math.ceil(len(self.full_options) / len(self.page_options)))
        self.page = min(max(0, self.page+val), num_pages)


        # Notify the menu (if it exists)
        if hasattr(self, 'menu'):
            self.page_options = self.menu.notify(self.full_options,self.page)


    def adjust_selection(self, val):
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
        if self.selected == len(self.page_options)-1:
            self.page = 0
            return self.page_options[-1]
        if self.main_menu:
            return self.most_recent_searches[self.selected]
        return 'play {0}'.format(self.selected + (len(self.page_options)*self.page))



    '''Attachments'''
    def attach_to_streamer(self,now_playing=None):
        self.streamer.attach(now_playing)

    def attach(self,menu=None):
        if menu is not None:
            self.menu = menu

    def exit(self):
        self.menu.__exit__()
