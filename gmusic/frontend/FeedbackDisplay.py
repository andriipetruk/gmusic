# -*- coding: utf-8 -*-
from gmusic.frontend.CursedObject import CursedObject
import curses
import math, time

class FeedbackDisplay(CursedObject):
    """Used for providing quick feedback to the user"""

    def __init__(self, win):
        self.screen = win
        self.time_elapsed = 0
        self.duration = 0
        self.is_random = False
        self.is_paused = False
        self.is_playing = False
        self.last_time = time.time()

        self.message = 'Default Feedback Message'
        self.is_showing_message = False
        self.message_start_time = time.time()
        self.message_duration = 1.0

    def accumulate_time(self):
        '''Used to continually accumulate time elapsed if playing'''
        if self.is_playing and not self.is_paused:
            self.time_elapsed += time.time() - self.last_time
        self.last_time = time.time()

    def display_message(self, message='Null message', duration=1.5):
        self.is_showing_message = True
        self.message = message
        self.message_start_time = time.time()
        self.message_duration = duration

    def new_song(self, duration):
        '''Reset everything for a new song'''
        self.is_playing = True
        self.is_paused = False
        self.is_showing_message = False
        self.time_elapsed = 0
        self.duration = duration
        self.last_time = time.time()

    def draw(self):
        '''Draw things!!!'''
        self.accumulate_time()
        self.determine_and_draw_feedback_type()

        self.screen.refresh()
        curses.setsyx(0, 0)
        curses.doupdate()


    def determine_and_draw_feedback_type(self):
        # If we're providing a message, do that first
        if self.is_showing_message:
            self.center_text('< {0} >'.format(self.message), 0)
            if time.time() > self.message_start_time + self.message_duration:
                self.is_showing_message = False
            return

        # If we're not playing, don't show anything
        if not self.is_playing:
            self.center_text(' ', 0)
            return

        # Otherwise, show the playing
        self.draw_playing()

    def draw_playing(self):
        '''This is what we draw if we are actually playing'''
        play = self.get_play_symbol()
        random = self.get_random_symbol()
        time_elapsed = self.format_time(int(self.time_elapsed))
        duration = self.format_time(self.duration)
        bar = self.get_bar()

        feedback_args = (play, time_elapsed, bar, duration, random)
        #self.screen.clrtoeol()
        self.screen.addstr(0, 2, '{0}[{1}]{2}[{3}]{4}'.format(*feedback_args))


    def format_time(self, value):
        '''Formats an int representing time, e.g. '13:52' '''
        formatted_length = 6
        result = '{0}:{1:02}'.format(int(math.floor(value/60)), value%60)

        left_pad_amount = int(math.floor((formatted_length-len(result)) / 2))
        right_pad_amount = formatted_length - len(result) - left_pad_amount

        return (' '*left_pad_amount) + result + (' '*right_pad_amount)

    def get_bar(self):
        '''Draws a progress bar depending on the time elapsed and duration'''
        bar_width = self.width() -30
        if self.duration == 0 or self.duration < self.time_elapsed:
            return ' '*bar_width

        # Now actually draw the bar
        progressed_bar = bar_width * self.time_elapsed/self.duration

        bar = '='*int(math.floor(progressed_bar))
        if (progressed_bar % 1) > 0.5:
            bar += '='
        else:
            bar += '-'
        bar += ' '*int(bar_width - len(bar))

        return bar

    def get_play_symbol(self):
        '''Returns either a play, pause, or null symbol depending on state'''
        if not self.is_playing:
            return '     '
        if self.is_paused:
            return ' ❚❚  '
        return '  ▶  '

    def get_random_symbol(self):
        '''Returns a random symbol if shuffling'''
        if self.is_random:
            return '  ¿? '
        return '     '
