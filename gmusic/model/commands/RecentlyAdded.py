from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class RecentlyAdded(Command):
    '''Searches for an artist'''

    def execute(self, *_):
        '''Gets the list of nids in the playlist, then loads information'''
        # ensures that data is accurate
        self.content_handler.recently_added()
