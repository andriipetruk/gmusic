from gmusic.core.EventHandler import EventHandler
from gmusic.frontend.Banner import Banner
from gmusic.frontend.CursedObject import CursedObject
from gmusic.frontend.FeedbackDisplay import FeedbackDisplay
from gmusic.frontend.Guide import Guide
from gmusic.frontend.Menu import Menu
from gmusic.frontend.UI import UI
import gmusic.model.events as events
import threading, time
import curses

class DrawHandler(CursedObject, EventHandler):
    def __init__(self, event_handler):
        EventHandler.__init__(self)
        self.attachments.append(event_handler)
        self.cache = event_handler.cache
        self.state = event_handler.state

    def launch(self, command_parser, ui_parser):
        self.start()
        self.create_system()
        self.screen.scrollok(False)
        self.screen.clear()
        self.screen.refresh()
        self.notify_attachments('Resize')
        self.draw()
        self.launch_threads(command_parser, ui_parser)

    def create_system(self):
        '''Builds all of the components and sends them the unified screen'''
        self.banner = Banner(self.screen)
        self.guide = Guide(self.screen)

        # Feedback
        feedback_start_x = 1
        feedback_start_y = 5
        feedback_width = self.width()-2
        feedback_height = 1
        feedback_win = curses.newwin(feedback_height, feedback_width, feedback_start_y, feedback_start_x)
        feedback_win.leaveok(1)
        self.feedback = FeedbackDisplay(feedback_win)

        # Menu
        menu_start_x = 1
        menu_start_y = 7
        menu_width = self.width() - 2
        menu_height = self.height() - 7 - 6 # 7 for banner/feedback, 6 for guide
        menu_win = curses.newwin(menu_height, menu_width, menu_start_y, menu_start_x)
        self.menu = Menu(menu_win)

    def resize_menu(self):
        menu_width = self.width() - 2
        menu_height = self.height() - 7 - 6 # 7 for banner/feedback, 6 for guide
        self.menu.screen.resize(menu_height, menu_width)

    def launch_threads(self, command_parser, ui_parser):
        """Launches a UI thread"""
        ui = UI(self, command_parser, ui_parser)
        ui_thread = threading.Thread(target=ui.__running__)
        ui_thread.start()

        refresh_thread = threading.Thread(target=self.refresh_thread)
        refresh_thread.daemon = True
        refresh_thread.start()

    def refresh_thread(self):
        while True:
            time.sleep(1.0)
            cur_pos = curses.getsyx()
            self.feedback.draw()
            curses.setsyx(*cur_pos)
            curses.doupdate()

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
        return self.menu.height() - 6

    def provide_feedback(self, information):
    #    self.feedback.draw(information)
        pass

    def handle_event(self, event, args=None):
        if isinstance(event, events.PageUpdate):
            self.redraw()

        if isinstance(event, events.PageChange):
            self.update_menu()
            self.redraw()

    def pause_or_resume(self, is_paused):
        self.feedback.is_paused = is_paused
        self.feedback.draw()

    def random(self, is_random):
        self.feedback.is_random = is_random
        self.feedback.draw()
