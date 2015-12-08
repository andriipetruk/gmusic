from gmusic.model.Event import Event

class EventHandler:
    def __init__(self):
        self.attachments = []

    def notify_attachments(self, event_class, event_parameters=None):
        '''Creates an event and sends it to capable attachments'''
        event = getattr(__import__('gmusic.model.events'), event_class)(self)

        if event_parameters is not None and type(event_parameters) is dict:
            self.build_event(event, event_parameters)

        # Iterate through every attachment to notify
        for attachment in self.attachments:
            self.try_notify(event, attachment)

    def build_event(self, event, event_parameters):
        '''Fleshes out the Event with parameters as specified'''
        build_gen = (p for p in event_parameters if hasattr(event, p))

        for parameter in build_gen:
            setattr(event, parameter, event_parameters[parameter])

    def try_notify(self, event, attachment):
        '''Notifies an attachment IF it is capable of handling an event'''
        if hasattr(attachment, 'handle_event'):
            attachment.handle_event(event)

    def handle_event(self, event):
        '''Must be defined in implementing class'''
        pass
