from gmusic.model.Command import Command

class Queue(Command):
    '''Tells the streamer's playlist to enqueue an id'''

    def execute(self, args):
        '''Enqueue an id'''
        if args is not None and 'id' in args:
            self.player_controller.queue(args['id'])
            return ('Feedback', {"message": 'Queued {0} for playback'.format(args['name']), "duration": 1.0})
