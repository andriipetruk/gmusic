class ContentHandler:
    def __init__(self):
        self.data_cache = DataCache()
        self.client = GMusicClient()

    def get_url(self, nid):
        '''Get URL for an nid'''
        return self.client.get_stream_url(nid)
