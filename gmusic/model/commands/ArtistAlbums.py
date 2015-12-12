from gmusic.model.Command import Command

class ArtistAlbums(Command):
    '''Searches for a artist's albums'''

    def execute(self, args):
        '''Asks the Content Manager to find all albums from an artist'''
        query = ''
        if args is not None and 'id' in args:
            query = args['id']
        self.content_handler.search_sub_items('artist', query)
