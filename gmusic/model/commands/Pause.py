from gmusic.model.Command import Command

class Pause(Command):
    '''Tells the streamer to pause playback'''

    def execute(self, *_):
        '''Tells the Streamer to pause/play toggle'''
        self.player_controller.pause()
