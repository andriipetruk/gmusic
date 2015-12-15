from gmusic.model.Command import Command

class SearchCommand(Command):
    '''Searches for an artist'''
    def __init__(self, *_):
        Command.__init__(self)
        self.search_type = 'songs'

    def pre_execute(self, args):
        if 'query' not in args:
            return ('Feedback', {'message': 'Displaying all {0}'.format(self.search_type)})

        query = args['query']
        if 'name' in args:
            query = args['name']
        return ('Feedback', {"message": 'Searching {0} matching "{1}"'.format(self.search_type, query)})

    def execute(self, args):
        '''Asks the Content Manager to find a song from specified artist'''
        query = ''
        if args is not None and 'query' in args:
            query = args['query']
        self.content_handler.search_items(self.search_type, query)
        return ('Feedback', {"is_showing_message": False})
