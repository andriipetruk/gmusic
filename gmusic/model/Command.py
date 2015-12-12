class Command:
    def __init__(self, *_):
        self.content_handler = None
        self.player_controller = None

    def pre_execute(self, args):
        pass

    def execute(self, query):
        pass
