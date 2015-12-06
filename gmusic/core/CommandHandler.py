class CommandHandler(object):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''

    def __init__(self, event_handler, content_handler, player_controller):
        self.attachments = [event_handler]
        self.content_handler = content_handler
        self.player_controller = player_controller

    def typed_radio(self, query):
        '''Gets a radio station'''
        radio = self.content_handler.search_radios(query)

    def typed_artist(self, artist):
        '''Asks the Content Manager to find a song from specified artist'''
        self.content_handler.search_items('artists', artist)

    def typed_song(self, song):
        '''Asks the Content Manager to find a song with a specified name'''
        self.content_handler.search_items('songs', song)

    def typed_album(self, album):
        '''Asks the Content Manager to find a song from specified album'''
        self.content_handler.search_items('albums', album)

    def typed_artist_albums(self, artist_id):
        self.content_handler.search_artist_or_album_items('artist', artist_id)

    def typed_album_songs(self, album_id):
        self.content_handler.search_artist_or_album_items('album', album_id)

    def typed_play(self, additional):
        '''Tells the streamer to play/resume or play a specific track'''
        if additional is "":
            self.player_controller.resume()
            return

        args = additional.split(' ', 1)
        if args[0] == 'radio':
            self.player_controller.play_radio(args[1])
        else:
            self.player_controller.play(args[1])

    def typed_stop(self, *_):
        '''Tells the streamer to stop playback'''
        self.player_controller.stop()

    def typed_pause(self, *_):
        '''Tells the Streamer to pause/play toggle'''
        self.player_controller.pause()

    def typed_resume(self, *_):
        '''Tells the streamer to resume'''
        self.player_controller.resume()

    def typed_previous(self, *_):
        '''Tells the menu to go to the previous song'''
        self.player_controller.previous()

    def typed_next(self, *_):
        '''Tells the Streamer to go to the next song'''
        self.player_controller.next()

    def typed_back(self, *_):
        self.notify_attachments('BACK')

    def typed_exit(self, *_):
        self.player_controller.stop()
        self.notify_attachments('EXIT')

    def typed_options(self, *_):
        self.notify_attachments('OPTIONS')

    def notify_attachments(self, event, args=None):
        for attachment in self.attachments:
            attachment.handle_event(event, args)
