from gmusic.model.Command import Command

class Suggested(Command):
    '''Get a list of songs suggested by Google'''

    def pre_execute(self, *_):
        return ('Feedback', {"message": 'Getting your suggested songs'})

    def execute(self, *_):
        self.content_handler.get_suggested()
        return ('Feedback', {"is_showing_message": False})
