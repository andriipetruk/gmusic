from gmusic.model.Command import Command

class Volume(Command):
    '''Tells the streamer to adjust playback volume'''

    def execute(self, args):
        adjustment = '0'
        if args is not None and 'adjustment' in args:
            adjustment = args['adjustment']
        self.player_controller.adjust_volume(float(adjustment))
        volume = self.player_controller.player.volume * 100.0
        return ('Feedback', {'message': 'Volume at {0}%'.format(volume), 'duration': 0.5})
