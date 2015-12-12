from gmusic.model.Command import Command

class Song(Command):
    '''Searches for a song'''

    def execute(self, args):
        '''Asks the Content Manager to find a playlist'''
        query = ''
        if args is not None and 'query' in args:
            query = args['query']
        self.content_handler.search_items('songs', query)
