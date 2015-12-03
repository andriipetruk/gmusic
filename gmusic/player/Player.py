import gst, gobject, thread

class Player:
    '''Direct interface with GStreamer; input ONLY from PlayerController'''

    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        self.build_bus()
        self.attachments = []

    def play(self, url):
        '''Play a track'''
        self.stop()
        #self.now_playing_track = track
        self.player.set_property('uri', url)
        self.player.set_state(gst.STATE_PLAYING)
        self.notify_attachments('START')

    def stop(self):
        '''Stop a song that is playing'''
        self.player.set_state(gst.STATE_NULL)

    def pause(self):
        '''Pause a song that is playing'''
        if gst.STATE_PAUSED == self.player.get_state()[1]:
            self.resume()
            return
        self.player.set_state(gst.STATE_PAUSED)

    def resume(self):
        '''Resume a song that has been paused'''
        self.player.set_state(gst.STATE_PLAYING)

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

    def notify_attachments(self, event):
        '''Send notifications to attachments'''
        for attachment in self.attachments:
            attachment.handle_event(event)

    #pylint: disable=unused-argument
    def handle_message(self, bus, message):
        '''Handles a message from gst'''
        if message.type == gst.MESSAGE_EOS:
            # file finished playing
            self.notify_attachments('END')
