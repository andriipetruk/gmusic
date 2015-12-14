from gmusic.model.Command import Command

class Radio(Command):
    '''Searches for a radio'''

    def execute(self, args=None):
        '''Gets a radio station'''
        query = ''
        if args is not None and 'id' in args:
            query = args['id']
            
        self.content_handler.search_radios(query)
