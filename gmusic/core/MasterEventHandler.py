from gmusic.core.EventHandler import EventHandler
from gmusic.core.Cache import Cache
from gmusic.core.State import State
from gmusic.frontend.DrawHandler import DrawHandler
import sys

class MasterEventHandler(EventHandler):
    def __init__(self):
        EventHandler.__init__(self)
        self.cache = Cache()
        self.state = State()
        self.draw_handler = DrawHandler(self.cache, self.state)

    def handle_event(self, event, args=None):
        if 'PAGE' in event:
            self.draw_handler.draw()
            return

        if 'CHANGE' in event:
            self.draw_handler.redraw()

        if 'PLAY' in event:
            self.draw_handler.banner_update(args)

        if 'RESUME' in event:
            self.draw_handler.banner_pause_resume(is_playing=True)

        if 'PAUSE' in event:
            self.draw_handler.banner_pause_resume(is_playing=False)

        if 'STOP' in event:
            self.draw_handler.banner_update(None)

        if 'OPTIONS' in event:
            self.state.options_menu()
            self.draw_handler.draw()

        if 'BACK' in event:
            self.state.main_menu()
            self.draw_handler.draw()

        if 'EXIT' in event:
            self.draw_handler.exit()
            sys.exit(1)

        if 'SEARCH' in event:
            self.state.state = event.split(' ', 1)[1]
            capacity = self.draw_handler.get_page_capacity()
            self.state.set_options(args, capacity)
            self.draw_handler.draw()

        if 'FEEDBACK' in event:
            self.draw_handler.provide_feedback(args[0])
