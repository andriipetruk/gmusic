from gmusic.model.Command import Command

class Options(Command):

    def execute(self, *_):
        '''Tells the Menu to go to main'''
        return ('ChangeMenu', {"menu_type": "options_menu"})
