from gmusic.content.ContentConsumer import ContentConsumer
from gmusicapi import Mobileclient
from decimal import Decimal
import json
import threading
import os

class GMusicClient(ContentConsumer):
    '''Element in charge of interfacing with GMusicApi Client'''

    def __init__(self, data_cache):
        self.client = Mobileclient()
        self.data_cache = data_cache

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        mac = Mobileclient.FROM_MAC_ADDRESS
        try:
            credentials = json.load(open('data/unlocked/credentials.json', 'r'))
            result = self.client.login(credentials['username'], credentials['password'], mac)
            if result == False:
                print('\n\033[93mLogin failed.')
                print('Please double check that data/unlocked/credentials.json has correct information.\033[m\n')
                os._exit(1)
        except:
            print('\n\033[93mdata/unlocked/credentials.json is not valid.')
            print('You may need to delete and regnerate the credentials file.\033[m\n')
            exit(1)

    def load_my_library(self):
        '''Load user's songs, playlists, and stations'''
        track_load = threading.Thread(target=self.load_tracks)
        radio_load = threading.Thread(target=self.load_radios)
        playlist_load = threading.Thread(target=self.load_playlists)

        track_load.start()
        radio_load.start()
        playlist_load.start()

        track_load.join()
        radio_load.join()
        playlist_load.join()

    def load_playlists(self):
        playlists = self.client.get_all_user_playlist_contents()
        playlists.reverse()
        self.data_cache.playlists = playlists

    def load_tracks(self):
        self.data_cache.tracks = [t for t in self.client.get_all_songs() if 'nid' in t]

    def scrape_song(self, track):
        return track

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
            return self.get_playlist_contents(from_id)

        else:
            # Get the appropriate search method and execute it
            search_method_name = 'get_{0}_info'.format(type_from)
            search_method = getattr(self.client, search_method_name)
            try:
                items = search_method(from_id, True)[args['type']+'s'] # True here includes subelements
            except:
                # User passed in a bad id or something
                return

        # Now return appropriately
        return [self.format_subitems(t, args) for t in items if args['id'] in t]

    def get_playlist_contents(self, from_id):
        '''Playlist exclusive stuff'''
        shareToken = [t for t in self.data_cache.playlists \
            if t['id'] == from_id][0]['shareToken']

        contents = self.client.get_shared_playlist_contents(shareToken)
        return [self.format_playlist_contents(t) for t in contents if 'track' in t]

    def get_suggested(self):
        '''Returns a list of tracks that the user might be interested in'''
        items = sorted(self.client.get_promoted_songs(), key=lambda y: y['title'])
        return [self.format_suggested(t) for t in items if 'storeId' in t]

    def get_information_about(self, from_type, from_id):
        '''Gets specific information about an id (depending on the type)'''
        if 'artist' in from_type.lower():
            return self.client.get_artist_info(from_id, include_albums=False)
        if 'album' in from_type.lower():
            return self.client.get_album_info(from_id, include_tracks=False)
        return self.client.get_track_info(from_id)

    def get_stream_url(self, nid):
        return self.client.get_stream_url(nid)

    def lookup(self, nid):
        return self.client.get_track_info(nid)

    def add_track_to_library(self, nid):
        self.client.add_aa_track(nid)

    def add_to_playlist(self, playlist_id, nid):
        self.client.add_songs_to_playlist(playlist_id, nid)

        playlist_load = threading.Thread(target=self.load_playlists)
        playlist_load.daemon = True
        playlist_load.start()

    def format_suggested(self, t):
        return (t['title'], t['storeId'], 'Play', t['album'])

    def format_playlist_contents(self, t):
        return (t['track']['title'], t['trackId'], 'Play', t['track']['album'])

    def format_subitems(self, t, args):
        return (t[args['name']], t[args['id']], args['command'], t[args['alt']])
