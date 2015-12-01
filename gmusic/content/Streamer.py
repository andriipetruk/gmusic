from gmusicapi import Mobileclient
import json, gst, gobject, thread

#pylint: disable=no-member
class Streamer(object):
    """Wrapper for GStreamer object"""

    def __init__(self):
        self.queue = []
        self.client = Mobileclient()
        self.player = gst.element_factory_make("playbin2", "player")
        self.now_playing_track = ""
        self.now_playing = None

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.handle_message)

    def run(self):
        '''Necessary for Messages to get sent'''
        self.login()
        gobject.threads_init()

        def start():
            '''Looping thread start'''
            loop = gobject.MainLoop()
            loop.run()
        thread.start_new_thread(start, ())

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        mac = Mobileclient.FROM_MAC_ADDRESS
        credentials = json.load(open('data/unlocked/credentials.json', 'r'))
        self.client.login(credentials['username'], credentials['password'], mac)



    def play_track(self, track):
        '''Play a URL'''
        if 'id' not in track:
            return
        self.stop()
        url = self.client.get_stream_url(track['id'])
        self.now_playing_track = track
        self.player.set_property('uri', url)
        self.player.set_state(gst.STATE_PLAYING)
        self.notify_attachments()

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

    def next(self):
        '''Play the next song'''
        self.player.set_state(gst.STATE_NULL)
        self.play_next()

    def next_in_queue(self):
        '''Get the next song in queue'''
        if len(self.queue) > 0:
            track = self.queue[0]
            self.queue.remove(track)
            return track
        return {"eos": True}

    #pylint: disable=unused-argument
    def handle_message(self, bus, message):
        '''Handles a message from gst'''
        if message.type == gst.MESSAGE_EOS:
            # file finished playing
            self.next()

    def play_next(self):
        '''Plays the next song in queue'''
        next_track = self.next_in_queue()
        self.play_track(next_track)
        self.notify_attachments()



    def attach(self, now_playing=None):
        '''Attaches an object for notification updates'''
        if now_playing is not None:
            self.now_playing = now_playing

    def notify_attachments(self):
        '''Send notifications to attachments'''
        if self.now_playing is not None:
            self.now_playing.draw(new_track=self.now_playing_track)
