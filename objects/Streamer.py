from gmusicapi import Mobileclient
import json, pygst, gst, sys, gobject, thread

class Streamer(object):

    '''STARTUP METHODS'''
    def __init__(self):
        self.queue = []
        self.client = Mobileclient()
        self.player = gst.element_factory_make("playbin2", "player")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.handle_message)

    def run(self):
        '''Necessary for Messages to get sent'''
        self.login()
        gobject.threads_init()

        def start():
            loop = gobject.MainLoop()
            loop.run()
        thread.start_new_thread(start, ())

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        credentials = json.load(open('data/unlocked/credentials.json','r'))
        self.logged_in = self.client.login(credentials['username'], credentials['password'], Mobileclient.FROM_MAC_ADDRESS)
        if self.logged_in:
            print 'Logged into Google Music\n'



    '''PLAYBACK METHODS'''
    def play_track(self, track):
        '''Play a URL'''
        self.stop()
        url = self.client.get_stream_url(track['id'])
        self.player.set_property('uri', url)

        self.player.set_state(gst.STATE_PLAYING)

    def resume(self):
        '''Resume a song that has been paused'''
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        '''Pause a song that is playing'''
        if gst.STATE_PAUSED == self.player.get_state()[1]:
            self.resume()
            return
        self.player.set_state(gst.STATE_PAUSED)

    def stop(self):
        '''Stop a song that is playing'''
        self.player.set_state(gst.STATE_NULL)



    '''MESSAGE METHODS'''
    def handle_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            # file finished playing
            self.player.set_state(gst.STATE_NULL)
            self.playback_finished()

    def playback_finished(self):
        if len(self.queue) > 0:
            track = self.queue[0]
            self.play_track(track)
            self.queue.remove(track)
