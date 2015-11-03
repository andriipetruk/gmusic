from gmusicapi import Mobileclient
from blessed import Terminal
import json
import pygst
import gst

def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print 'on_tag:'
    for key in taglist.keys():
        print '\t%s = %s' % (key, taglist[key])

class GoogleMusicTerminal(object):
    def __init__(self):
        self.terminal = Terminal()
        self.credentials = json.load(open('data/unlocked/credentials.json','r'))
        self.client = Mobileclient()
        self.last_search_tracks = []

        # Player
        self.player = gst.element_factory_make("playbin", "player")

    def login(self):
        self.logged_in = self.client.login(self.credentials['username'], self.credentials['password'], Mobileclient.FROM_MAC_ADDRESS)
        self.songs = self.client.get_all_songs()

    def get(self, song="", artist=""):
        '''Attempts to print '''
        if not self.logged_in:
            print("Not logged in!")
            return

        self.last_search_tracks = [s for s in self.songs if (artist in s['artist'] and song in s['title'])]
            #self.last_search_tracks = {:self.client.get_stream_url(s['id'])  }
        print self.terminal.clear() + "Search Results\n========================="

        for i in range(0,len(self.last_search_tracks)):
            print('[{0}]:  "{1}" by {2}'.format(i, self.terminal.bold(self.last_search_tracks[i]['title']), self.last_search_tracks[i]['artist']))

    def play(self,index):
        if index > len(self.last_search_tracks):
            print "Index out of range."
            return

        track = self.last_search_tracks[index]

        print self.terminal.clear() + 'Now Playing "{0}" by {1}\n=========================='.format(self.terminal.bold(track['title']), track['artist'])
        self.play_url(self.client.get_stream_url(track['id']))



    def play_url(self, url):
        #start playing
        self.player.set_property('uri', url)
        self.player.set_state(gst.STATE_PLAYING)

        #listen for tags on the message bus; tag event might be called more than once
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message::tag', on_tag)
