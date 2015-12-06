from gmusicapi import Mobileclient
import json

class GMusicClient:
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
        self.data_cache.add_tracks(self.client.get_all_songs())
        self.data_cache.add_radios(self.client.get_all_stations())

    def get_radio_contents(self, radio_id):
        tracks = self.client.get_station_tracks(radio_id)
        return tracks

    def get_radio_list(self, name):
        return [r for r in self.data_cache.radios if name in r['name']]

    def filter(self, element, field, filter_by):
        return [e for e in element if filter_by in e[field]]

    def get_playlist_list(self, name):
        return self.filter(self.playlists, 'name', name)

    def search_all_access(self, query):
        return self.client.search_all_access(query)

    def get_index_arguments(self, type):
        '''Get the data indexing arguments'''
        # Songs have some weird arguments, so we have to account for that
        if type is 'songs':
            return {'type': 'track',
            'name': 'title',
            'id': 'nid',
            'alt': 'album'}

        # Otherwise we can generalize a lot of data
        return {'type': type[:-1],
            'name': 'name',
            'id': type[:-1]+'Id',
            'alt': 'artist'}

    def format_item(self, item, type, args):
        '''Format the item for content_handler'''
        # Artist does not have alternate information
        if type is 'artists':
            return (item[args['type']][args['name']], \
                item[args['type']][args['id']], \
                None)

        # Otherwise include alternate information
        return (item[args['type']][args['name']], \
            item[args['type']][args['id']], \
            item[args['type']][args['alt']])

    def search_items_all_access(self, query, type):
        '''Searches Albums, Artists, and Songs; uses metaprogramming'''
        index_arguments = self.get_index_arguments(type)

        items = self.search_all_access(query)['{0}_hits'.format(type[:-1])]
        return [self.format_item(item, type, index_arguments) for item in items]

    def get_album_songs(self, album_id):
        songs = self.client.get_album_info(album_id, include_tracks=True)['tracks']
        return [(t['title'], t['nid'], t['album']) for t in songs if 'nid' in t]

    def get_artist_albums(self, artist_id):
        albums = self.client.get_artist_info(artist_id, include_albums=True)['albums']
        return [(t['name'], t['albumId'], t['artist']) for t in albums if 'albumId' in t]

    def get_stream_url(self, nid):
        return self.client.get_stream_url(nid)

    def lookup(self, nid):
        return self.client.get_track_info(nid)
