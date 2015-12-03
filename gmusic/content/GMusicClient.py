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

    def search_tracks_all_access(self, query):
        return self.search_all_access(query)['song_hits']

    def search_artists_all_access(self, query):
        artists = self.search_all_access(query)['artist_hits']
        return [(artist['artist']['name'], artist['artist']['artistId']) for artist in artists]

    def search_albums_all_access(self, query):
        return self.search_all_access(query)['album_hits']

    def get_stream_url(self, nid):
        return self.client.get_stream_url(nid)

    def lookup(self, nid):
        return self.client.get_track_info(nid)
