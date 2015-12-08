from gmusic.model.Event import Event

class EventHandler:
    def __init__(self):
        self.attachments = []

    def notify_attachments(self, event_string, options=None):
        '''Creates an event and sends it to capable attachments'''
        event = Event(event_string, self, options)

        # Iterate through every attachment to notify
        for attachment in self.attachments:
            self.try_notify(event, attachment)

    def try_notify(self, event, attachment):
        '''Notifies an attachment IF it is capable of handling an event'''
        if hasattr(attachment, 'handle_event'):
            attachment.handle_event(event)
