from gmusic.content.DataCache import DataCache
from gmusic.content.GMusicClient import GMusicClient

class ContentHandler:
    def __init__(self):
        self.attachments = []
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

    def search_artists(self, artist):
        if artist is not '':
            artists = self.client.search_artists_all_access(artist)
        else:
            artists = self.data_cache.get_artists()
        self.notify_attachments('SEARCH Artists', artists)

    def search_albums(self, album):
        if album is not '':
            albums = self.client.search_albums_all_access(album)
        else:
            albums = self.data_cache.get_albums()
        self.notify_attachments('SEARCH Albums', albums)

    def search_radios(self, query):
        sorted_radios = sorted(self.client.get_radio_list(query), reverse=True, key = lambda x : x['recentTimestamp'])
        radios = [(r['name'], r['id']) for r in sorted_radios]
        self.notify_attachments('SEARCH Radios', radios)

    def search_songs(self, song):
        if song is not '':
            songs = self.client.search_tracks_all_access(song)
        else:
            songs = self.data_cache.get_tracks()
        self.notify_attachments('SEARCH Songs', songs)

    def notify_attachments(self, event, args=None):
        for attachment in self.attachments:
            attachment.handle_event(event, args)
