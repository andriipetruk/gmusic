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

    def play_song_from_list(self, nid):
        '''Play a song from SEARCH Songs'''
        # Since these are stored, they should already be nids
        nids = self.content_handler.data_cache.recently_searched_songs
        self.load(nids)

        # Error handling: if there's a fluke and this nid isn't in the list
        # play it, then play the playlist.
        if nid in nids:
            self.playlist.index = nids.index(nid)
        else:
            self.playlist.index = 0
        self.play(nid)

    def adjust_volume(self, adjustment):
        self.player.adjust_volume(adjustment)

    def handle_event(self, event):
        '''Handle events from Player'''
        if 'END' in event:
            self.next()
        self.notify_attachments(event)

    def previous(self):
        '''Play the next song'''
        prev_song = self.playlist.previous()
        self.play(prev_song)

    def random(self):
        self.playlist.toggle_random()

    def next(self):
        '''Play the next song'''
        next_song = self.playlist.next()
        self.play(next_song)

    def play(self, nid):
        '''Plays a song using an nid as lookup'''
        try:
            url = self.content_handler.get_url(nid)
        except:
            self.next()
            return

        self.player.play(url)

        # Tell attachments about the song
        track_details = self.content_handler.lookup_nid(nid)
        self.notify_attachments('PLAY', track_details)

    def stop(self):
        self.player.stop()
        self.notify_attachments('STOP')

    def resume(self):
        self.player.resume()
        self.notify_attachments('PLAY')

    def pause(self):
        self.player.pause()

    def load(self, playlist):
        '''Loads a playlist of nids'''
        self.playlist.load(playlist)

    def track_details(self, nid):
        '''Gets a full object from Content'''
        return self.content_manager.lookup_nid(nid)

    def notify_attachments(self, event, args=None):
        for attachment in self.attachments:
            attachment.handle_event(event, args)
