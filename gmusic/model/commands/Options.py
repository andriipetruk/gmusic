from gmusic.model.Command import Command
from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State
import json

class Options(Command):

    def execute(self, *_):
        '''Tells the Menu to go to main'''
        with open('configuration/settings.json','r') as settings:
        	data = json.load(settings)

        elements = [MenuElement(data['options'][s]['description'], 'Configure', alt=str(data['options'][s]['value'])) for s in data['options']]

        options_state = State("Options Menu", "Options", elements)
        options_state.id = 'options'
        return ('PushState', {"state": options_state})
