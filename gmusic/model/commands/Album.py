from gmusic.model.Command import Command

class Album(Command):
    '''Searches for an album'''

    def execute(self, args):
        '''Asks the Content Manager to find a song from specified album'''
        query = ''
        if args is not None and 'query' in args:
            query = args['query']
        self.content_handler.search_items('albums', query)
