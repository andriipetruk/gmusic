from gmusic.content.ContentConsumer import ContentConsumer
from gmusicapi import Mobileclient
from decimal import Decimal
import json

class GMusicClient(ContentConsumer):
    '''Element in charge of interfacing with GMusicApi Client'''

    def __init__(self, data_cache):
        self.client = Mobileclient()
        self.data_cache = data_cache

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        mac = Mobileclient.FROM_MAC_ADDRESS
        credentials = json.load(open('data/unlocked/credentials.json', 'r'))
        self.client.login(credentials['username'], credentials['password'], mac)

    def load_my_library(self):
        '''Load user's songs, playlists, and stations'''
        self.load_tracks()
        self.load_radios()
        self.load_playlists()

    def load_playlists(self):
        playlists = self.client.get_all_user_playlist_contents()
        playlists.reverse()
        self.data_cache.playlists = playlists

    def load_tracks(self):
        tracks = [t for t in self.client.get_all_songs() if 'nid' in t]
        self.data_cache.tracks = tracks

    def load_radios(self):
        radios = self.client.get_all_stations()
        radios.reverse()
        self.data_cache.radios = radios

    def get_radio_contents(self, radio_id):
        tracks = self.client.get_station_tracks(radio_id)
        return tracks

    def get_radio_list(self, name):
        return [r for r in self.data_cache.radios if name in r['name']]

    def filter(self, element, field, filter_by):
        return [e for e in element if filter_by in e[field]]

    def get_playlist_list(self, name):
        return self.filter(self.data_cache.playlists, 'name', name)

    def search_all_access(self, query):
        return self.client.search_all_access(query)

    def create_radio(self, seed_type, id, name):
        '''Create a radio'''
        # This is a weird way to do this, but there's no other choice
        ids = {"track": None, "album": None, "artist": None}
        seed_id_name = self.get_type_name(seed_type)
        ids[seed_id_name] = id
        return self.client.create_station(name=name, track_id=ids['track'], album_id=ids['album'], artist_id=ids['artist'])

    def search_items_all_access(self, type, query):
        '''Searches Albums, Artists, and Songs; uses metaprogramming'''
        index_arguments = self.get_index_arguments(type)

        items = self.search_all_access(query)['{0}_hits'.format(type[:-1])]
        return [self.format_item(item, type, index_arguments) for item in items]

    def get_sub_items(self, type_from, search_type, from_id):
        '''Here type_from refers to artist or album we're indexing against'''
        args = self.get_index_arguments(search_type)

        if type_from == 'playlist':
            args['id'] = 'storeId'
            items = self.get_playlist_contents(from_id)

        else:
            # Get the appropriate search method and execute it
            search_method_name = 'get_{0}_info'.format(type_from)
            search_method = getattr(self.client, search_method_name)
            items = search_method(from_id, True)[args['type']+'s'] # True here includes subelements

        # Now return appropriately
        return [(t[args['name']], t[args['id']], t[args['alt']])\
            for t in items if args['id'] in t]

    def get_playlist_contents(self, from_id):
        '''Playlist exclusive stuff'''
        items = [t for t in self.data_cache.playlists \
            if t['id'] == from_id][0]['tracks']
        return [t['track'] for t in items if 'track' in t]

    def get_suggested(self):
        '''Returns a list of tracks that the user might be interested in'''
        items = sorted(self.client.get_promoted_songs(), key=lambda y: y['title'])
        return [(t['title'], t['storeId'], t['album']) for t in items if 'storeId' in t]

    def get_stream_url(self, nid):
        return self.client.get_stream_url(nid)

    def lookup(self, nid):
        return self.client.get_track_info(nid)
