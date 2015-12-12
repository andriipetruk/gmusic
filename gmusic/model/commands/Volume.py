from gmusic.model.Command import Command

class Volume(Command):
    '''Tells the streamer to adjust playback volume'''

    def execute(self, args):
        adjustment = '0'
        if args is not None and 'adjustment' in args:
            adjustment = args['adjustment']
        self.player_controller.adjust_volume(float(adjustment))
