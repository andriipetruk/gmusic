from gmusic.model.Command import Command

class PlayRadio(Command):
    '''Tells the streamer to play/resume or play a specific track'''

    def pre_execute(self, args):
        '''Seeds a station from an artist, album, or track'''
        # ensures that data is accurate
        if 'id' not in args:
            return

        return ('Feedback', {"message": 'Loading {0} for playback'.format(args['name'])})

    def execute(self, args):
        if 'id' not in args:
            self.player_controller.resume()
            return

        self.player_controller.play_radio(args['id'])
        return ('Feedback', {"is_showing_message": False})
