from gmusic.model.Command import Command

class Playlist(Command):
    '''Searches for a playlist'''

    def execute(self, args):
        '''Asks the Content Manager to find a playlist'''
        query = ''
        if args is not None and 'id' in args:
            query = args['id']

        self.content_handler.search_playlists(query)
