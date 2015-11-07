from objects.Display import Display
import sys

class Interpreter(object):
    def __init__(self, streamer, display):
        self.streamer = streamer
        self.display = display
        self.last_search_tracks = []

    def typed_artist(self, artist=""):
        '''Attempts to print '''
        self.search(artist=artist)

    def typed_song(self, song=""):
        '''Attempts to print '''
        self.search(song=song)

    def typed_album(self, album=""):
        '''Attempts to print '''
        self.search(album=album)

    def search(self,artist="",album="",song=""):
        self.last_search_tracks = [s for s in self.streamer.songs if (album in s['album'] and artist in s['artist'] and song in s['title'])]
        self.display.search_results(self.last_search_tracks)


    def typed_play(self,index):
        '''Play a song using an index from the most recent search'''
        # Make sure it is within range
        if int(index) > len(self.last_search_tracks):
            print "Index out of range."
            return

        track = self.last_search_tracks[int(index)]
        self.display.now_playing(track)
        self.streamer.play_url(self.streamer.client.get_stream_url(track['id']))

    def typed_stop(self,ignored):
        self.streamer.stop()

    def typed_pause(self,ignored):
        self.streamer.pause()

    def typed_resume(self,ignored):
        self.streamer.resume()

    def typed_exit(self, ignored):
        self.display.clear()
        sys.exit(1)

    def typed_help(self, ignored):
        self.display.help()
