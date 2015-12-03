import curses

class UIHandler(object):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''
    def __init__(self, event_handler, command_handler):
        self.attachments = [event_handler]
        self.state = event_handler.state
        self.cache = event_handler.cache
        self.cmd_handler = command_handler

    def handle(self, user_in):
        # Enter Key
        if user_in == 10:
            return self.handle_execute()

        # Escape
        if user_in == 27:
            pass
        #self.exit()

        # Spacebar
        if user_in == ord(' '):
            cmd_handler.typed_pause()

        # n (next)
        if user_in == ord('n'):
            self.cmd_handler.typed_next()

        # p (prev)
        if user_in == ord('p'):
            self.cmd_handler.typed_previous()

        # Page Increment/Decrement
        if user_in == ord('['):
            self.state.change_page(-1)
            self.notify_attachments('PAGE CHANGE')
        if user_in == ord(']'):
            self.state.change_page(1)
            self.notify_attachments('PAGE CHANGE')


        # Increment or Decrement
        if user_in == curses.KEY_DOWN: # down arrow
            self.state.adjust_selection(1)
            self.notify_attachments('SELECTION CHANGE')
        if user_in == curses.KEY_UP: # up arrow
            self.state.adjust_selection(-1)
            self.notify_attachments('SELECTION CHANGE')

    def adjust_selection(self, val):
        pass


    def handle_execute(self):
        pass

    def notify_attachments(self, event):
        '''blahblah'''
        for attachment in attachments:
            attachment.handle_event(event)
