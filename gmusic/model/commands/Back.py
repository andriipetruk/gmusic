from gmusic.model.Command import Command

class Back(Command):

    def execute(self, *_):
        '''Tells the Menu to go back a page'''
        return ('PopMenu', None)
