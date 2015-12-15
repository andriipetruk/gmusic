from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class AddToPlaylist(Command):
    '''Searches for an artist'''

    def execute(self, args):
        '''Asks the Content Manager to find a playlist'''
        if not set([a for a in args]).issuperset(['stored_id','name','id']):
            return

        self.content_handler.client.add_to_playlist(args['id'], args['stored_id'])
        return ('Feedback', {'message': 'Added to playlist {0}'.format(args['name'])})

    def post_execute(self, *_):
        return ('PopState', None)
