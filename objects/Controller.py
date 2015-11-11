from objects.Display import Display
import sys

class Controller(object):
    def __init__(self, streamer, content_manager):
        self.streamer = streamer
        self.content_manager = content_manager

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
        track = self.content_manager.play_track(int(index))
        self.streamer.queue = self.content_manager.search_results
        self.streamer.play_track(track)

    def typed_stop(self,ignored=""):
        self.streamer.stop()

    def typed_pause(self,ignored=""):
        self.streamer.pause()

    def typed_resume(self,ignored=""):
        self.streamer.resume()

    def typed_back(self,ignored=""):
        self.content_manager.search_menu = False
