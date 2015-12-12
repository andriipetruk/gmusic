from gmusic.model.Command import Command

class Next(Command):
    '''Tells the streamer to go to next song'''

    def execute(self, *_):
        self.player_controller.next()
