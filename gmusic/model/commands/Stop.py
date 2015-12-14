from gmusic.model.Command import Command

class Stop(Command):
    '''Tells the streamer to stop playback'''

    def execute(self, *_):
        self.player_controller.stop()
