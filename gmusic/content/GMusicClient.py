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
        self.playlists = self.client.get_all_playlists()

    def get_radio(self, name):
        pass

    def get_radio_list(self, name):
        return self.filter(self.radios, 'name', name)

    def get_playlist(self):
        pass

    def get_playlist_list(self, name):
        return self.filter(self.playlists, 'name', name)

    def search(self):
        pass

    def filter(self, element, field, filter_by):
        return [e for e in element if filter_by in e[field]]
