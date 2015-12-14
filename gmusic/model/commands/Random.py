from gmusic.model.Command import Command

class Random(Command):
    '''Tells the streamer to randomize set list'''

    def execute(self, *_):
        '''Tells the Streamer that we want to toggle random'''
        self.player_controller.random()
