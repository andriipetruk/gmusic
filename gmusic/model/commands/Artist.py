from gmusic.model.Command import Command

class Artist(Command):
    '''Searches for an artist'''

    def execute(self, args):
        '''Asks the Content Manager to find a song from specified artist'''
        query = ''
        if args is not None and 'query' in args:
            query = args['query']
        self.content_handler.search_items('artists', query)
