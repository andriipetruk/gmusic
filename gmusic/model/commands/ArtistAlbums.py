from gmusic.model.SubelementSearchCommand import SubelementSearchCommand

class ArtistAlbums(SubelementSearchCommand):
    '''Searches for a artist's albums'''

    def __init__(self, *_):
        SubelementSearchCommand.__init__(self)
        self.search_type = 'album'
        self.origin_type = 'artist'
