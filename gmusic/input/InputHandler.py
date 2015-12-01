class InputHandler(object):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''

    def __init__(self, content_manager):
        self.content_manager = content_manager

    def typed_artist(self, artist):
        '''Asks the Content Manager to find a song from specified artist'''
        self.content_manager.search_songs(artist=artist)

    def typed_song(self, song):
        '''Asks the Content Manager to find a song with a specified name'''
        self.content_manager.search_songs(song=song)

    def typed_album(self, album):
        '''Asks the Content Manager to find a song from specified album'''
        self.content_manager.search_songs(album=album)

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
        self.content_manager.streamer.stop()

    def typed_pause(self, *_):
        '''Tells the Streamer to pause/play toggle'''
        self.content_manager.streamer.pause()

    def typed_resume(self, *_):
        '''Tells the streamer to resume'''
        self.content_manager.streamer.resume()

    def typed_back(self, *_):
        '''Tells the menu to return to main menu'''
        self.content_manager.back_to_main()

    def typed_next(self, *_):
        '''Tells the Streamer to go to the next song'''
        self.content_manager.streamer.next()
