from gmusic.model.SearchCommand import SearchCommand

class Artist(SearchCommand):
    '''Searches for an artist'''
    def __init__(self, *_):
        SearchCommand.__init__(self)
        self.search_type = 'artists'
