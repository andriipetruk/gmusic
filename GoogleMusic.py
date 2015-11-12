from objects.Streamer import Streamer
from objects.Interface import Interface

class GoogleMusic(object):
    '''Google Music Terminal Interface'''
    def __init__(self):
        self.interface = Interface()

    def __start__(self):
        self.interface.__running__()
