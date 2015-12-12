from gmusic.model.commands.PlayRadio import PlayRadio
from gmusic.model.Command import Command

class Seed(Command):
    '''Creates and seeds a radio from a song'''

    def pre_execute(self, args):
        '''Seeds a station from an artist, album, or track'''
        # ensures that data is accurate
        if not set([a for a in args]).issuperset(['type', 'id', 'name']):
            return ('Feedback', {"message": 'Incorrect data provided for seed'})

        return ('Feedback', {"message": 'Creating Radio "{0}"'.format(args['name'])})

    def execute(self, args):
        radio_id = self.content_handler.create_radio(args['type'], args['id'], args['name'])
        if radio_id is None:
            return ('Feedback', {'message': 'There was an issue in creating radio "{0}"'.format(name)})

        play = PlayRadio()
        play.player_controller = self.player_controller
        play.execute({'id': radio_id})
        return ('Feedback', {'message': 'Created successfully'})
