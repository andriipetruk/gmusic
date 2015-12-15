from gmusic.core.EventHandler import EventHandler
from gmusic.model.commands import *
import curses

class UIHandler(EventHandler):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''
    def __init__(self, event_handler, cmd_processor):
        EventHandler.__init__(self)
        self.attachments.append(event_handler)
        self.state = event_handler.state
        self.cache = event_handler.cache
        self.cmd_processor = cmd_processor

    def handle(self, user_in):
        # Enter Key
        if user_in == 10:
            execution_command = self.state.handle_execute()
            if execution_command is not None:
                self.cmd_processor.process(*execution_command)

        if user_in == curses.KEY_RESIZE:
            self.notify_attachments('Resize')

        # Spacebar
        if user_in == ord(' '):
            self.cmd_processor.process('Pause')

        # n (next)
        if user_in == ord('n'):
            self.cmd_processor.process('Next')

        # p (prev)
        if user_in == ord('p'):
            self.cmd_processor.process("Previous")

        if user_in == ord('a'):
            if self.state.current_state_is('songs'):
                id = self.state.get_selected_element().id
                name = self.state.get_selected_element().main
                self.cmd_processor.process('AddTo', {"id": id, 'name': name})

        # Queue
        if user_in == ord('q'):
            id = self.state.get_selected_element().id
            self.cmd_processor.process('Queue', {'id': id})

        if user_in == ord('+'):
            self.cmd_processor.process('Volume',  {'adjustment': 0.10})
        if user_in == ord('-'):
            self.cmd_processor.process('Volume',  {'adjustment': -0.10})

        if user_in == ord('r') or user_in == ord('R'):
            # Seed Radio
            seed_type = self.state.get_seed_type()
            if seed_type is not '':
                id = self.state.get_selected_element().id
                name = self.state.get_selected_element().main
                cmd = ('Seed', {"id": id, 'name': name, 'type': seed_type})
                self.cmd_processor.process(*cmd)
            else:
                self.notify_attachments('Feedback', {'message': "Error in state {0}".format(seed_type)})

        # Increment or Decrement
        if user_in == curses.KEY_DOWN: # down arrow
            self.state.adjust_selection(1)
            self.notify_attachments('PageUpdate')
        if user_in == curses.KEY_UP: # up arrow
            self.state.adjust_selection(-1)
            self.notify_attachments('PageUpdate')
        if user_in == curses.KEY_RIGHT:
            self.state.change_page(1)
            self.notify_attachments('PageChange')
        if user_in == curses.KEY_LEFT:
            self.state.change_page(-1)
            self.notify_attachments('PageChange')
