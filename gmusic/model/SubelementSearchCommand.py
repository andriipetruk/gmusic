from gmusic.model.SearchCommand import SearchCommand

class SubelementSearchCommand(SearchCommand):
    '''Searches for an artist'''
    def __init__(self, *_):
        SearchCommand.__init__(self)
        self.origin_type = 'Nothing'

    def pre_execute(self, args):
        return ('Feedback', {"message": 'Fetching all {0}s from {1}'.format(self.search_type, args['name'])})

    def execute(self, args):
        '''Asks the Content Manager to find a song from specified artist'''
        query = ''
        if args is not None and 'id' in args:
            query = args['id']
        self.content_handler.search_sub_items(self.origin_type, query)
        return ('Feedback', {"is_showing_message": False})
