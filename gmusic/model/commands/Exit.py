from gmusic.model.Command import Command

class Exit(Command):

    def execute(self, *_):
        '''Tells the application to exit'''
        self.player_controller.stop()
        return ('ProgramExit', None)
