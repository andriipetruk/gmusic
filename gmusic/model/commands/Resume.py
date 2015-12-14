from gmusic.model.Command import Command

class Resume(Command):
    '''Tells the streamer to resume playback'''

    def execute(self, *_):
        '''Tells the Streamer to resume'''
        self.player_controller.resume()
