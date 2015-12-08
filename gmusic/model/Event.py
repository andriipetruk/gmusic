class Event:
    def __init__(self, sender, details, parameters=None):
        self.sender = sender
        self.details = details
        self.parameters = parameters
