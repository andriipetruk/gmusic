from gmusic.player.PlayList import PlayList
from gmusic.player.Player import Player
from gmusic.content.ContentHandler import ContentHandler
import json

#pylint: disable=no-member
class PlayerController(object):
    '''Controls Player; operable by Menu and remote DJ'''

    def __init__(self):
        self.playlist = PlayList()
        self.content_handler = None
        self.player = Player()
        self.player.attachments.append(self)

    def handle_event(self, event):
        '''Handle events from Player'''
        if 'END' in event:
            self.next()

    def next(self):
        '''Play the next song'''
        next_song = self.playlist.next()
        url = self.content_handler.get_url(next_song)
        self.player.play(url)

    def play(self):
        pass

    def pause(self):
        self.player.pause()
