from gmusic.model import State

class Command(State):
    '''Represents any menu-relevant command state'''

    def __init__(self, command):
        State.__init__(self)
        self.command = command
