from gmusic.core.EventHandler import EventHandler
from gmusic.model.events import *
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import thread
Gst.init(None)

class Player(EventHandler):
    '''Direct interface with GStreamer; input ONLY from PlayerController'''

    def __init__(self):
        EventHandler.__init__(self)
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.volume = 1.0
        self.build_bus()

    def play(self, url):
        '''Play a track'''
        self.stop()
        self.player.set_property('uri', url)
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        '''Stop a song that is playing'''
        self.player.set_state(Gst.State.NULL)
        self.notify_attachments('PlayOrStop',{"track": None})

    def pause(self):
        '''Pause a song that is playing'''
        if Gst.State.PAUSED == self.player.get_state(Gst.CLOCK_TIME_NONE)[1]:
            self.resume()
            return
        self.player.set_state(Gst.State.PAUSED)
        self.notify_attachments('PauseOrResume',{"is_paused": True})

    def resume(self):
        '''Resume a song that has been paused'''
        self.player.set_state(Gst.State.PLAYING)
        self.notify_attachments('PauseOrResume',{"is_paused": False})

    def adjust_volume(self, adjustment):
        self.volume = max(min(1.5, self.volume + float(adjustment)), 0.0)
        self.player.set_property('volume', self.volume)

    def build_bus(self):
        '''Handle building the bus'''
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.handle_message)

    def run(self):
        '''Necessary for Messages to get sent'''
        GObject.threads_init()

        def start():
            '''Looping thread start'''
            loop = GObject.MainLoop()
            loop.run()
        thread.start_new_thread(start, ())

    #pylint: disable=unused-argument
    def handle_message(self, bus, message):
        '''Handles a message from Gst'''
        if message.type == Gst.MessageType.EOS:
            # file finished playing
            self.notify_attachments('EndOfStream')
