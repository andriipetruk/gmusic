from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class Options(Command):

    def execute(self, *_):
        '''Tells the Menu to go to main'''
        elements = [
            MenuElement('Volume adjustment amount', command='Back', alt='10%'),
            MenuElement('Number of radio tracks to pull', command='Back', alt='25'),
            MenuElement('Port for DJ Notifications', command='Back', alt='8080'),
            MenuElement('Allow DJ to control playback', command='Back', alt='No'),
            MenuElement('Back', command='Back')]
        options_state = State("Options Menu", "Options", elements)
        options_state.id = 'options'
        return ('PushState', {"state": options_state})
