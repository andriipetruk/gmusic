from gmusic.content.DataCache import DataCache
from gmusic.content.GMusicClient import GMusicClient
from gmusic.core.EventHandler import EventHandler
from gmusic.model.MenuElement import MenuElement

class ContentHandler(EventHandler):
    def __init__(self):
        EventHandler.__init__(self)
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
            return self.data_cache.get_item_from_id('track', nid)

        # Not in cache; need to look it up
        return self.client.lookup(nid)

    def create_radio(self, seed_type, id, name):
        '''Create a radio from an id, then add it to cache'''
        radio_id = self.client.create_radio(seed_type, id, name)
        self.client.load_radios()
        return radio_id

    def search_radios(self, query):
        self.search_radio_or_playlist(query, 'radios')

    def search_playlists(self, query):
        self.search_radio_or_playlist(query, 'playlists')

    def search_radio_or_playlist(self, query, type):
        method_name = 'get_{0}_list'.format(type[:-1])
        search = getattr(self.client, method_name)

        items = [MenuElement(r['name'], r['id']) for r in search(query)]
        self.notify_attachments('Search',\
            event_parameters={"results": items,
            "title": query,
            "display_element_type": "{0}".format(type.capitalize())} )

    def search_items(self, search_type, query):
        '''Master Search Method'''
        if query is not '':
            method_name = 'search_items_all_access'.format(search_type)
            search = getattr(self.client, method_name)
        else:
            method_name = 'get_items'.format(search_type)
            search = getattr(self.data_cache, method_name)

        found_items = search(search_type, query)
        self.package_and_notify(query, search_type, found_items)

    def package_and_notify(self, title, search_type, found_items):
        '''Stores in data cache if it's a song, then packages and notifies'''
        if 'song' in search_type:
            self.data_cache.recently_searched_songs = [x[1] for x in found_items]
        items = [MenuElement(s[0], s[1], s[2]) for s in found_items]
        if len(items) > 0:
            self.notify_attachments('Search',\
                event_parameters={"results": items,
                "title": title,
                "display_element_type": "{0}".format(search_type.capitalize())})

    def search_sub_items(self, type_from, from_id):
        '''Works for getting a specific artist's albums, or an album's tracks'''
        search_type = 'songs'
        if type_from is 'artist':
            search_type = 'albums'

        found_items = self.client.get_sub_items(type_from, search_type, from_id)
        self.package_and_notify(from_id, search_type, found_items)

    def get_suggested(self):
        '''Gets a list of tracks that the user might be interested in'''
        suggested_tracks = self.client.get_suggested()
        self.package_and_notify('Suggested Tracks', 'songs', suggested_tracks)
