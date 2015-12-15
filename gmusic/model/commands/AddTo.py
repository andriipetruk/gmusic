from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class AddTo(Command):
    '''Searches for an artist'''

    def execute(self, args):
        '''Gets the list of nids in the playlist, then loads information'''
        # ensures that data is accurate
        if not set([a for a in args]).issuperset(['id', 'name']):
            return

        elements = [
            MenuElement('Queue', command='Queue'),
            MenuElement('Library', command='AddToLibrary'),
            MenuElement('Playlist', command='AddToPlaylistPrompt')]

        for e in elements:
            e.id = args['id']

        state = State("Add {0} to...".format(args['name']), "Options", elements)
        state.id = 'addto'

        return ('PushState', {'state': state})
