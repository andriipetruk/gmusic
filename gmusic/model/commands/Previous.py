from gmusic.model.Command import Command

class Previous(Command):

    def execute(self, *_):
        '''Tells the streamer to go to the previous song'''
        self.player_controller.previous()
