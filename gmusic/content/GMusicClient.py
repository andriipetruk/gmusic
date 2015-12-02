from gmusicapi import Mobileclient
import json

class GMusicClient:
    def __init__(self):
        self.client = Mobileclient()

    def login(self):
        '''Use data/unlocked/credentials.json to log in'''
        mac = Mobileclient.FROM_MAC_ADDRESS
        credentials = json.load(open('credentials.json', 'r'))
        self.client.login(credentials['username'], credentials['password'], mac)

    def load_my_library(self):
        '''Load user's songs, playlists, and stations'''
        self.songs = self.client.get_all_songs()
        self.radios = self.client.get_all_stations()

    def get_radio_contents(self, radio_id):
        tracks = self.client.get_station_tracks(radio_id)
        return tracks

    def get_radio_list(self, name):
        return self.filter(self.radios, 'name', name)

    def filter(self, element, field, filter_by):
        return [e for e in element if filter_by in e[field]]

    def get_playlist_list(self, name):
        return self.filter(self.playlists, 'name', name)

    def search_all_access(self, query):
        return self.client.search_all_access(query)

    def search_tracks_all_access(self, query):
        return self.search_all_access(query)['song_hits']

    def search_artists_all_access(self, query):
        return self.search_all_access(query)['artist_hits']

    def search_albums_all_access(self, query):
        return self.search_all_access(query)['album_hits']
