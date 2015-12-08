from gmusic.core.EventHandler import EventHandler
from gmusic.model.events import *
import gst, gobject, thread

class Player(EventHandler):
    '''Direct interface with GStreamer; input ONLY from PlayerController'''

    def __init__(self):
        EventHandler.__init__(self)
        self.player = gst.element_factory_make("playbin2", "player")
        self.volume = 1.0
        self.build_bus()

    def play(self, url):
        '''Play a track'''
        self.stop()
        self.player.set_property('uri', url)
        self.player.set_state(gst.STATE_PLAYING)
        #self.notify_attachments('PauseOrResume',{"is_playing": True})

    def stop(self):
        '''Stop a song that is playing'''
        self.player.set_state(gst.STATE_NULL)
        self.notify_attachments('PlayOrStop',{"track": None})

    def pause(self):
        '''Pause a song that is playing'''
        if gst.STATE_PAUSED == self.player.get_state()[1]:
            self.resume()
            return
        self.player.set_state(gst.STATE_PAUSED)
        self.notify_attachments('PauseOrResume',{"is_playing": False})

    def resume(self):
        '''Resume a song that has been paused'''
        self.player.set_state(gst.STATE_PLAYING)
        self.notify_attachments('PauseOrResume',{"is_playing": True})

    def adjust_volume(self, adjustment):
        self.volume = max(min(2.0,self.volume + float(adjustment)/10.0), 0.0)
        self.player.set_property('volume', self.volume)

    def build_bus(self):
        '''Handle building the bus'''
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.handle_message)

    def run(self):
        '''Necessary for Messages to get sent'''
        gobject.threads_init()

        def start():
            '''Looping thread start'''
            loop = gobject.MainLoop()
            loop.run()
        thread.start_new_thread(start, ())

    #pylint: disable=unused-argument
    def handle_message(self, bus, message):
        '''Handles a message from gst'''
        if message.type == gst.MESSAGE_EOS:
            # file finished playing
            self.notify_attachments('EndOfStream')
