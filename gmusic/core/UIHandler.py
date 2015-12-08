from gmusic.core.EventHandler import EventHandler
import curses

class UIHandler(EventHandler):
    '''Text-Entry Controller which interfaces with Streamer/ContentManager'''
    def __init__(self, event_handler, cmd_parser):
        EventHandler.__init__(self)
        self.attachments.append(event_handler)
        self.state = event_handler.state
        self.cache = event_handler.cache
        self.cmd_parser = cmd_parser

    def handle(self, user_in):
        # Enter Key
        if user_in == 10:
            execution_command = self.state.handle_execute()
            if execution_command is not "":
                self.cmd_parser.parse(execution_command)

        # Spacebar
        if user_in == ord(' '):
            self.cmd_parser.parse("pause")

        # n (next)
        if user_in == ord('n'):
            self.cmd_parser.parse("next")

        # p (prev)
        if user_in == ord('p'):
            self.cmd_parser.parse("previous")

        # Queue
        if user_in == ord('q'):
            id = self.state.get_selected_element().id
            self.cmd_parser.parse('queue {0}'.format(id))

        if user_in == ord('+'):
            self.cmd_parser.parse('volume 1')
        if user_in == ord('-'):
            self.cmd_parser.parse('volume -1')

        if user_in == ord('r') or user_in == ord('R'):
            # Seed Radio
            seed_type = self.state.get_seed_type()
            if seed_type is not '':
                id = self.state.get_selected_element().id
                name = self.state.get_selected_element().main
                cmd = 'seed {0} {1} {2}'.format(seed_type, id, name)
                self.cmd_parser.parse(cmd)

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
