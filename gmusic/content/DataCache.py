#from gmusic.player.Streamer import Streamer
from gmusic.content.ContentConsumer import ContentConsumer
import math

class DataCache(ContentConsumer):
    def __init__(self):
        self.tracks = []
        self.radios = []
        self.playlists = []
        self.recently_searched_songs = []

    def has_track(self, nid):
        '''Checks to see if an nid exists in the cache'''
        return nid in self.track_id_list()

    def has_radio(self, rid):
        '''Checks to see if an rid exists in the cache'''
        return rid in self.radio_id_list()

    def radio_id_list(self):
        '''Creates a list of nids'''
        return [radio['id'] for radio in self.radios if 'id' in radio]

    def track_id_list(self):
        '''Creates a list of nids'''
        return [track['nid'] for track in self.tracks if 'nid' in track]

    def get_item_from_id(self, item_type, id):
        '''Get an item which matches a specific id'''
        id_type = self.get_id_type(item_type)
        target = self.get_cache_target(item_type)
        return [x for x in target if id_type in x and x[id_type] == id][0]

    def get_cache_target(self, item_type):
        '''Used to determine the data_cache source for searching'''
        if 'radio' in item_type:
            return self.radios
        if 'playlist' in item_type:
            return self.playlists
        return self.tracks

    def get_items(self, item_type, *_):
        '''Get all items from cache of `item_type`'''
        args = self.get_index_arguments(item_type)
        items = self.get_cache_target(item_type)
        gen = (item for item in items if args['id'] in item)

        if 'song' in item_type or 'track' in item_type:
            args['type'] = 'title'

        # Have to account for absurdity in 'artists' AGAIN...
        if item_type == 'artists':
            return list(set([self.format_artist(artist, args) for artist in gen]))
        return list(set([self.format_result(item, args) for item in gen]))

    def recently_added(self):
        args = self.get_index_arguments('songs')
        args['type'] = 'title'
        return [self.format_result(a, args) for a in sorted(self.tracks, reverse=True, \
            key=lambda y: y['creationTimestamp']) \
            if ('creationTimestamp' in a and 'deleted' in a)]

    def format_result(self, item, args):
        return (item[args['type']], item[args['id']], args['command'], item[args['alt']])

    def format_artist(self, artist, args):
        return (artist[args['type']], artist[args['id']][0], 'ArtistAlbums', None)
