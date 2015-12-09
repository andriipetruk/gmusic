from gmusic.core.EventHandler import EventHandler
from gmusic.model.events import *
from gmusic.frontend.Banner import Banner
from gmusic.frontend.CursedObject import CursedObject
from gmusic.frontend.FeedbackDisplay import FeedbackDisplay
from gmusic.frontend.Guide import Guide
from gmusic.frontend.Menu import Menu
from gmusic.frontend.UI import UI
import threading, time
import curses

class DrawHandler(CursedObject, EventHandler):
    def __init__(self, cache, state):
        self.cache = cache
        self.state = state

    def launch(self, command_parser, ui_parser):
        self.start()
        self.create_system()
        self.screen.clear()
        self.screen.refresh()
        self.draw()
        self.launch_threads(command_parser, ui_parser)

    def create_system(self):
        '''Builds all of the components and sends them the unified screen'''
        self.banner = Banner(self.screen)
        self.guide = Guide(self.screen)
        win = curses.newwin(1, self.width()-2, 5, 1)
        win.leaveok(1)
        self.feedback = FeedbackDisplay(win)
        self.menu = Menu(self.screen)

    def launch_threads(self, command_parser, ui_parser):
        """Launches a UI thread"""
        ui = UI(self, command_parser, ui_parser)
        ui_thread = threading.Thread(target=ui.__running__)
        ui_thread.start()

        feedback_thread = threading.Thread(target=self.feedback.time_thread)
        feedback_thread.daemon = True
        feedback_thread.start()

        refresh_thread = threading.Thread(target=self.refresh_thread)
        refresh_thread.daemon = True
        refresh_thread.start()

    def refresh_thread(self):
        while True:
            time.sleep(0.5)
            self.screen.leaveok(1)
            self.screen.refresh()
            self.feedback.draw()

    def draw(self):
        self.screen.clear()
        self.screen.refresh()
        self.update_menu()
        self.redraw()

    def update_menu(self):
        self.menu.options = self.state.page_elements
        self.menu.title = self.state.title
        self.menu.subtitle = self.state.subtitle

    def redraw(self):
        self.menu.draw(selected=self.state.selected_element)
        self.screen.refresh()
        self.banner.draw()
        self.feedback.draw()
        self.guide.draw()

    def banner_update(self, song_details):
        if song_details is not None:
            self.feedback.new_song( int(song_details['durationMillis']) / 1000 )
        else:
            self.feedback.is_playing = False

        self.banner.track = song_details
        self.feedback.draw()
        self.banner.draw()

    def get_page_capacity(self):
        return self.height() - 17

    def provide_feedback(self, information):
    #    self.feedback.draw(information)
        pass

    def handle_event(self, event, args=None):
        if isinstance(event, PageUpdate):
            self.redraw()

        if isinstance(event, PageChange):
            self.update_menu()
            self.redraw()

    def pause_or_resume(self, is_paused):
        self.feedback.is_paused = is_paused
        self.feedback.draw()

    def random(self, is_random):
        self.feedback.is_random = is_random
        self.feedback.draw()
