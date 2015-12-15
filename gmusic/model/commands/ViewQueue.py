from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class ViewQueue(Command):
    '''Searches for an artist'''

    def pre_execute(self, *_):
        return ('Feedback', {'message': 'Fetching Queue'})

    def execute(self, *_):
        '''Gets the list of nids in the playlist, then loads information'''
        queue = self.player_controller.playlist.contents
        items = [self.content_handler.lookup_nid(nid) for nid in queue]

        menu_items = [MenuElement(*self.format_song(item)) for item in items]
        state = State("Queued Songs", "queue", menu_items)

        return ('Search', {'state': state})

    def format_song(self, song):
        return (song['title'], song['nid'], 'Play', song['artist'])
