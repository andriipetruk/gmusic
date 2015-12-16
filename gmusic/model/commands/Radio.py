from gmusic.model.Command import Command

class Radio(Command):
    '''Searches for a radio'''

    def pre_execute(self, args):
        if 'query' in args:
            return ('Feedback', {"message": 'Searching radios matching "{0}"'.format(args['query'])})

    def execute(self, args=None):
        '''Gets a radio station'''
        query = ''
        if args is not None and 'query' in args:
            query = args['query']

        self.content_handler.search_radios(query)
        return ('Feedback', {"is_showing_message": False})
