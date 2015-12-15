from gmusic.model.Command import Command
from gmusic.model.InterimState import InterimState

class AddToPlaylistPrompt(Command):
    '''Searches for an artist'''

    def pre_execute(self, args):
        state = InterimState(command='AddToPlaylist', stored_id=args['id'])
        return ('SetInterimState', {'state': state})

    def execute(self, *_):
        '''Asks the Content Manager to find a playlist'''
        self.content_handler.search_playlists('')
