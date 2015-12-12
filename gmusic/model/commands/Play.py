from gmusic.model.Command import Command

class Play(Command):
    '''Tells the streamer to play/resume or play a specific track'''

    def pre_execute(self, args):
        '''Seeds a station from an artist, album, or track'''
        # ensures that data is accurate
        if 'id' not in args:
            return

        return ('Feedback', {"message": 'Loading song for playback'})

    def execute(self, args):
        if 'id' not in args:
            self.player_controller.resume()
            return

        self.player_controller.play_song_from_list(args['id'])
