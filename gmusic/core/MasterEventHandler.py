from gmusic.core.EventHandler import EventHandler
from gmusic.core.Cache import Cache
from gmusic.core.StateManager import StateManager
from gmusic.frontend.DrawHandler import DrawHandler
import gmusic.model.events as events
import sys

class MasterEventHandler(EventHandler):
    def __init__(self):
        EventHandler.__init__(self)
        self.cache = Cache()
        self.state = StateManager()
        self.draw_handler = DrawHandler(self)

    def handle_event(self, event):
        if isinstance(event, events.PageChange):
            self.draw_handler.draw()

        if isinstance(event, events.PageUpdate):
            self.draw_handler.redraw()

        if isinstance(event, events.PlayOrStop):
            self.draw_handler.banner_update(event.track)

        if isinstance(event, events.PauseOrResume):
            self.draw_handler.pause_or_resume(event.is_paused)

        if isinstance(event, events.ToggleRandom):
            self.draw_handler.random(event.is_random)

        if isinstance(event, events.ChangeMenu):
            build_menu = getattr(self.state, event.menu_type)
            build_menu()
            self.draw_handler.draw()

        if isinstance(event, events.Resize):
            capacity = self.draw_handler.get_page_capacity()
            self.state.capacity = capacity
            self.draw_handler.draw()

        if isinstance(event, events.PopState):
            self.state.pop_state()
            self.draw_handler.draw()

        if isinstance(event, events.SetInterimState):
            self.state.interim_state = event.state

        if isinstance(event, events.ProgramExit):
            self.draw_handler.exit()
            sys.exit(1)

        if isinstance(event, events.PushState):
            self.state.push_state(event.state)
            self.draw_handler.draw()

        if isinstance(event, events.Feedback):
            self.draw_handler.feedback.display_message(event.message, event.duration)
            self.draw_handler.feedback.is_showing_message = event.is_showing_message
            self.draw_handler.feedback.draw()
