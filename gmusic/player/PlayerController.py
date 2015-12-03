from gmusic.player.PlayList import PlayList
from gmusic.player.Player import Player
from gmusic.content.ContentHandler import ContentHandler
import json

#pylint: disable=no-member
class PlayerController(object):
    '''Controls Player; operable by Menu and remote DJ'''

    def __init__(self, content_handler):
        self.playlist = PlayList()
        self.content_handler = content_handler
        self.player = Player()
        self.player.attachments.append(self)
        self.attachments = []

    def start(self):
        '''Start up the system'''
        self.player.run()

    def play_radio(self, rid):
        '''Plays a radio station by indexing with an rid'''
        tracks = self.content_handler.client.get_radio_contents(rid)
        nids = [track['nid'] for track in tracks if 'nid' in track]
        self.load(nids)
        self.play(nids[0])

    def handle_event(self, event):
        '''Handle events from Player'''
        if 'END' in event:
            self.next()

    def previous(self):
        '''Play the next song'''
        prev_song = self.playlist.previous()
        self.play(prev_song)

    def next(self):
        '''Play the next song'''
        next_song = self.playlist.next()
        self.play(next_song)

    def play(self, nid):
        '''Plays a song using an nid as lookup'''
        url = self.content_handler.get_url(nid)
        self.player.play(url)
        self.notify_attachments('PLAY')

    def pause(self):
        self.player.pause()
        self.notify_attachments('PAUSE')

    def load(self, playlist):
        '''Loads a playlist of nids'''
        self.playlist.load(playlist)

    def track_details(self, nid):
        '''Gets a full object from Content'''
        return self.content_manager.lookup_nid(nid)

    def notify_attachments(self, event):
        for attachment in self.attachments:
            attachment.handle_event(event)
