class ContentManager(object):

    def __init__(self, streamer):
        self.streamer = streamer
        self.songs = []
        self.radios = []
        self.search_results =[]
        self.title = ''
        self.subtitle = ''
        self.search_menu = False
        self.most_recent_searches = []
        self.now_playing_track = ""
        self.redraw = False

    def load(self):
        print "Loading songs and radios.\n"
        self.songs = self.streamer.client.get_all_songs()
        self.radios = self.streamer.client.get_all_stations()

    def search_songs(self,artist="",album="",song=""):
        search_results = [s for s in self.songs if (album.lower() in s['album'].lower() and artist.lower() in s['artist'].lower() and song.lower() in s['title'].lower())]
        if len(search_results) > 0:
            self.title = artist+album+song
            self.subtitle = "Search Results"
            self.search_menu = True
            self.redraw = True
            self.search_results = search_results

    def get_most_recent_searches(self):
        return self.most_recent_searches + ['Options', 'Exit']

    def play_track(self, num):
        track = self.search_results[num]
        self.now_playing_track = track
        self.redraw = True
        return track

    def queue(self, track_index):
        queue = []
        if track_index < len(self.search_results):
            queue += self.search_results[track_index+1:]
        if track_index > 0:
             queue += self.search_results[:track_index-1]

        self.streamer.queue = queue
