from gmusic.model.Command import Command

class PlaylistSongs(Command):
    '''Searches for a playlist's songs'''

    def execute(self, args):
        query = ''
        if args is not None and 'id' in args:
            query = args['id']
        self.content_handler.search_sub_items('playlist', query)
