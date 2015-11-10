from objects.Display import Display
import sys

class Interpreter(object):
    def __init__(self, streamer, content_manager):
        self.streamer = streamer
        self.content_manager = content_manager
        self.last_search_tracks = []

    '''Search Functions'''
    def typed_artist(self, artist=""):
        '''Attempts to print '''
        self.content_manager.search_songs(artist=artist)

    def typed_song(self, song=""):
        '''Attempts to print '''
        self.content_manager.search_songs(song=song)

    def typed_album(self, album=""):
        '''Attempts to print '''
        self.content_manager.search_songs(album=album)

    '''Playback Control Functions'''
    def typed_play(self,index):
        '''Play a song using an index from the most recent search'''
        track = self.content_manager.search_results[int(index)]
        self.streamer.play_url(self.streamer.client.get_stream_url(track['id']))

    def typed_stop(self,ignored):
        self.streamer.stop()

    def typed_pause(self,ignored):
        self.streamer.pause()

    def typed_resume(self,ignored):
        self.streamer.resume()

    def typed_back(self,ignored):
        self.content_manager.search_menu = False
