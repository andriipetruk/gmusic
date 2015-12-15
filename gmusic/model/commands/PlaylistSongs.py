from gmusic.model.SubelementSearchCommand import SubelementSearchCommand

class PlaylistSongs(SubelementSearchCommand):
    '''Searches for a artist's albums'''

    def __init__(self, *_):
        SubelementSearchCommand.__init__(self)
        self.search_type = 'song'
        self.origin_type = 'playlist'
