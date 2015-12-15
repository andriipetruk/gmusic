from gmusic.model.SearchCommand import SearchCommand

class Album(SearchCommand):
    '''Searches for an album'''
    def __init__(self, *_):
        SearchCommand.__init__(self)
        self.search_type = 'albums'
