from gmusic.core.EventHandler import EventHandler
from gmusic.core.Cache import Cache
from gmusic.core.StateManager import StateManager
from gmusic.frontend.DrawHandler import DrawHandler
from gmusic.model.events import *
import sys

class MasterEventHandler(EventHandler):
    def __init__(self):
        EventHandler.__init__(self)
        self.cache = Cache()
        self.state = StateManager()
        self.draw_handler = DrawHandler(self)

    def handle_event(self, event):
        if isinstance(event, PageChange):
            self.draw_handler.draw()

        if isinstance(event, PageUpdate):
            self.draw_handler.redraw()

        if isinstance(event, PlayOrStop):
            self.draw_handler.banner_update(event.track)

        if isinstance(event, PauseOrResume):
            self.draw_handler.pause_or_resume(event.is_paused)

        if isinstance(event, Random):
            self.draw_handler.random(event.is_random)

        if isinstance(event, ChangeMenu):
            build_menu = getattr(self.state, event.menu_type)
            build_menu()
            self.draw_handler.draw()

        if isinstance(event, Resize):
            capacity = self.draw_handler.get_page_capacity()
            self.state.capacity = capacity
            self.draw_handler.draw()

        if isinstance(event, Back):
            self.state.pop_state()
            self.draw_handler.draw()

        if isinstance(event, Exit):
            self.draw_handler.exit()
            sys.exit(1)

        if isinstance(event, Search):
            self.state.push_state(event.state)
            self.draw_handler.draw()

        if isinstance(event, Feedback):
            self.draw_handler.feedback.message = event.message
            self.draw_handler.feedback.is_showing_message = True
            self.draw_handler.feedback.draw()
