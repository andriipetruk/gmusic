from gmusic.model.Command import Command

class Queue(Command):
    '''Tells the streamer's playlist to enqueue an id'''

    def execute(self, args):
        '''Enqueue an id'''
        query = ''
        if args is not None and 'id' in args:
            id = args['id']
        self.player_controller.queue(id)
        return ('Feedback', {"message": 'Queued song for playback'})
