#from gmusic.player.Streamer import Streamer
import math

class DataCache:
    def __init__(self):
        self.tracks = []
        self.radios = []

    def has_track(self, nid):
        '''Checks to see if an nid exists in the cache'''
        return nid in self.track_nid_list()

    def get_track(self, nid):
        '''Gets the track which matches this nid'''
        return [x for x in self.tracks if 'nid' in x and x['nid'] == nid][0]

    def add_tracks(self, tracks):
        '''Adds tracks to the cache'''
        self.tracks = self.tracks + tracks

    def track_nid_list(self):
        '''Creates a list of nids'''
        return [track['nid'] for track in self.tracks if 'nid' in track]

    def has_radio(self, rid):
        '''Checks to see if an rid exists in the cache'''
        return rid in self.radio_rid_list()

    def get_radio(self, rid):
        '''Gets the station which matches this id'''
        return [x for x in self.radios if 'id' in x and x['id'] == rid][0]

    def add_radios(self, radios):
        '''Adds tracks to the cache'''
        self.radios = self.radios + radios

    def radio_rid_list(self):
        '''Creates a list of nids'''
        return [radio['id'] for radio in self.radios if 'id' in radio]

    def get_albums(self, *_):
        return list(set([(track['album'],track['albumId'],track['artist']) \
            for track in self.tracks if 'albumId' in track]))

    def get_artists(self, *_):
        return list(set([(track['artist'],track['artistId'][0],None) \
            for track in self.tracks if 'artistId' in track]))

    def get_tracks(self, *_):
        return [(track['title'], track['nid'], track['album'])\
            for track in self.tracks if 'nid' in track]
