#from gmusic.player.Streamer import Streamer
from gmusic.content.ContentConsumer import ContentConsumer
import math

class DataCache(ContentConsumer):
    def __init__(self):
        self.tracks = []
        self.radios = [];
        self.recently_searched_songs = []

    def has_track(self, nid):
        '''Checks to see if an nid exists in the cache'''
        return nid in self.track_id_list()

    def has_radio(self, rid):
        '''Checks to see if an rid exists in the cache'''
        return rid in self.radio_id_list()

    def add_tracks(self, tracks):
        '''Adds tracks to the cache'''
        self.tracks = self.tracks + tracks

    def add_radios(self, radios):
        '''Adds tracks to the cache'''
        self.radios = self.radios + radios

    def radio_id_list(self):
        '''Creates a list of nids'''
        return [radio['id'] for radio in self.radios if 'id' in radio]

    def track_id_list(self):
        '''Creates a list of nids'''
        return [track['nid'] for track in self.tracks if 'nid' in track]

    def get_item_from_id(self, item_type, id):
        '''Get an item which matches a specific id'''
        id_type = self.get_id_type(item_type)
        return [x for x in self.tracks if id_type in x and x[id_type] == id][0]

    def get_cache_target(self, item_type):
        '''Used to determine the data_cache source for searching'''
        if 'radio' in item_type:
            return self.radios
        return self.tracks

    def get_items(self, item_type, *_):
        '''Get all items from cache of `item_type`'''
        args = self.get_index_arguments(item_type)

        # Have to account for absurdity in 'artists' AGAIN...
        if item_type == 'artists':
            return list(set([(track[args['type']], track[args['id']][0], None) \
                for track in self.tracks if args['id'] in track]))

        if 'song' in item_type or 'track' in item_type:
            args['type'] = 'title'

        return list(set([(track[args['type']], track[args['id']], track[args['alt']]) \
            for track in self.get_cache_target(item_type) if args['id'] in track]))
