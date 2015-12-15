from gmusic.model.SubelementSearchCommand import SubelementSearchCommand

class AlbumSongs(SubelementSearchCommand):
    '''Searches for a artist's albums'''

    def __init__(self, *_):
        SubelementSearchCommand.__init__(self)
        self.search_type = 'song'
        self.origin_type = 'album'
