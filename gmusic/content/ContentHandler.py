from gmusic.content.DataCache import DataCache
from gmusic.content.GMusicClient import GMusicClient
from gmusic.MenuElement import MenuElement

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

    def search_radios(self, query):
        sorted_radios = sorted(self.client.get_radio_list(query), reverse=True, key = lambda x : x['recentTimestamp'])
        radios = [MenuElement(r['name'], r['id']) for r in sorted_radios]
        self.notify_attachments('SEARCH Radios', radios)

    def search_items(self, search_type, query):
        '''Master Search Method'''
        if query is not '':
            method_name = 'search_items_all_access'.format(search_type)
            search = getattr(self.client, method_name)
        else:
            method_name = 'get_{0}'.format(search_type)
            search = getattr(self.data_cache, method_name)

        items = [MenuElement(s[0], s[1], s[2]) for s in search(query, search_type)]
        if len(items) > 0:
            self.notify_attachments('SEARCH {0}'.format(search_type.capitalize()), items)

    def search_artist_albums(self, artist_id):
        found_albums = self.client.get_artist_albums(artist_id)

        #Package
        albums = [MenuElement(s[0],s[1],s[2]) for s in found_albums]
        self.notify_attachments('SEARCH Albums', albums)

    def search_album_songs(self, album_id):
        found_songs = self.client.get_album_songs(album_id)

        #Package
        songs = [MenuElement(s[0],s[1],s[2]) for s in found_songs]
        self.notify_attachments('SEARCH Songs', songs)

    def notify_attachments(self, event, args=None):
        for attachment in self.attachments:
            attachment.handle_event(event, args)
