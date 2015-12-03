class CommandHandler(object):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''

    def __init__(self, content_handler, player_controller):
        self.content_handler = content_handler
        self.player_controller = player_controller

    def typed_radio(self, query):
        '''Gets a radio station'''
        radio = self.content_handler.client.get_radio_list(query)
        self.player_controller.play_radio(radio[0]['id'])

    def typed_artist(self, artist):
        '''Asks the Content Manager to find a song from specified artist'''
        self.content_handler.search_songs(artist=artist)

    def typed_song(self, song):
        '''Asks the Content Manager to find a song with a specified name'''
        self.content_handler.search_songs(song=song)

    def typed_album(self, album):
        '''Asks the Content Manager to find a song from specified album'''
        self.content_handler.search_songs(album=album)

    def typed_play(self, index=""):
        '''Tells the streamer to play/resume or play a specific track'''
        if index is "":
            self.content_manager.streamer.resume()
            return

        #Play a song using an index from the most recent search
        track = self.content_manager.play_track(int(index))
        self.content_manager.queue(int(index))
        self.content_manager.streamer.play_track(track)

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
