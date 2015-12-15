from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class AddToLibrary(Command):
    '''Searches for an artist'''

    def execute(self, args):
        '''Gets the list of nids in the playlist, then loads information'''
        # ensures that data is accurate
        if 'id' not in args:
            return

        self.content_handler.client.add_track_to_library(args['id'])
        return ('Feedback', {'message':'Track added to library'})
