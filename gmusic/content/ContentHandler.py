from gmusic.content.DataCache import DataCache
from gmusic.content.GMusicClient import GMusicClient

class ContentHandler:
    def __init__(self):
        self.data_cache = DataCache()
        self.client = GMusicClient(self.data_cache)

    def launch(self):
        self.client.login()
        self.client.load_my_library()

    def get_url(self, nid):
        '''Get URL for an nid'''
        return self.client.get_stream_url(nid)

    def lookup_nid(self, nid):
        '''Try to get information about an nid'''
        # Check to see if it's in our library
        if self.data_cache.has_track(nid):
            return self.data_cache.get_track(nid)

        # Not in cache; need to look it up
        return self.client.lookup(nid)

    def lookup_rid(self, rid):
        '''Try to get information about a radio id'''
        if self.data_cache.has_track(rid):
            return self.data_cache.get_radio(rid)
