from objects.Streamer import Streamer
from objects.Interface import Interface

class GoogleMusic(object):
    '''Google Music Terminal Interface'''
    def __init__(self):
        self.streamer = Streamer()
        self.interface = Interface(self.streamer)

    def __start__(self):
        self.streamer.login()
        self.interface.__running__()
