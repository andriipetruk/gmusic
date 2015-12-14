from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class Options(Command):

    def execute(self, *_):
        '''Tells the Menu to go to main'''
        elements = [
            MenuElement('Background color', id='', command='Back', alt='Gray'),
            MenuElement('Text color', id='', command='Back', alt='White'),
            MenuElement('Highlight color', id='', command='Back', alt='White'),
            MenuElement('Number of radio tracks to pull', id='', command='Back', alt='25'),
            MenuElement('Port for DJ Notifications', id='', command='Back', alt='8080'),
            MenuElement('Allow DJ to control playback', id='', command='Back', alt='No')]
        options_state = State("Options Menu", "Options", elements)
        options_state.id = 'options'
        return ('PushState', {"state": options_state})
