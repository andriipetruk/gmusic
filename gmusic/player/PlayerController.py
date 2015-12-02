from gmusic.player.PlayList import PlayList
from gmusic.player.Player import Player
from gmusic.content.ContentHandler import ContentHandler
import json

#pylint: disable=no-member
class PlayerController(object):
    '''Controls Player; operable by Menu and remote DJ'''

    def __init__(self):
        self.playlist = PlayList()
        self.content_handler = ContentHandler()
        self.player = Player()
        self.player.attachments.append(self)

    def handle_event(self, event):
        '''Handle events from Player'''
        if 'END' in event:
            self.next()

    def next(self):
        '''Play the next song'''
        next_song = self.playlist.next()
        self.play(next_song)

    def play(self, nid):
        '''Plays a song using an nid as lookup'''
        url = self.content_handler.get_url(nid)
        self.player.play(url)

    def pause(self):
        self.player.pause()

    def load_playlist(self, playlist):
        '''Loads a playlist of nids'''
        self.playlist.load(playlist)

    def track_details(self, nid):
        '''Gets a full object from Content'''
        return self.content_manager.lookup_nid(nid)
