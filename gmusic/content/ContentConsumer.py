class ContentConsumer:
    '''Basic item for working with Content (e.g. DataCache and Client)'''

    def get_index_arguments(self, type):
        '''Get the data indexing arguments'''
        # Songs have some weird arguments, so we have to account for that
        if type is 'songs':
            return {'type': 'track',
            'name': 'title',
            'id': 'nid',
            'alt': 'album'}

        # Otherwise we can generalize a lot of data
        return {'type': type[:-1],
            'name': 'name',
            'id': self.get_id_type(type[:-1]),
            'alt': 'artist'}

    def format_item(self, item, type, args):
        '''Format the item for content_handler'''
        # Artist does not have alternate information
        if type is 'artists':
            return (item[args['type']][args['name']], \
                item[args['type']][args['id']], \
                None)

        # Otherwise include alternate information
        return (item[args['type']][args['name']], \
            item[args['type']][args['id']], \
            item[args['type']][args['alt']])

    def get_id_type(self, type):
        '''Returns the name of the field which is used for indexing this type'''
        if 'song' in type or 'track' in type:
            return 'nid'
        if 'radio' in type:
            return 'id'
        return type + 'Id'
