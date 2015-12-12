from gmusic.model.Command import Command

class Main(Command):

    def execute(self, *_):
        '''Tells the Menu to go to main'''
        return ('ChangeMenu', None)
