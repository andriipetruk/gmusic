from gmusicapi import Mobileclient
import json, pygst, gst, sys

class Streamer(object):
    def __init__(self):
        self.last_search_tracks = []
        self.client = Mobileclient()
        self.player = gst.element_factory_make("playbin", "player")

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        credentials = json.load(open('data/unlocked/credentials.json','r'))
        self.logged_in = self.client.login(credentials['username'], credentials['password'], Mobileclient.FROM_MAC_ADDRESS)
        self.songs = self.client.get_all_songs()
        
    def play_url(self, url):
        '''Play a URL'''
        self.stop()
        self.player.set_property('uri', url)
        self.player.set_state(gst.STATE_PLAYING)

        ##listen for tags on the message bus; tag event might be called more than once
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()

    def resume(self):
        '''Resume a song that has been paused'''
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        '''Pause a song that is playing'''
        self.player.set_state(gst.STATE_PAUSED)

    def stop(self):
        '''Stop a song that is playing'''
        self.player.set_state(gst.STATE_NULL)
