from gmusic.model.Command import Command

class AlbumSongs(Command):
    '''Searches for a album's songs'''

    def execute(self, args):
        '''Asks the Content Manager to find all songs from an album'''
        query = ''
        if args is not None and 'id' in args:
            query = args['id']
        self.content_handler.search_sub_items('album', query)
