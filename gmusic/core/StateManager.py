from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State

class StateManager(object):
    def __init__(self):
        self.state = ""
        self.title = ""
        self.subtitle = ""
        self.selected_element = 0
        self.page_number = 0
        self.capacity = 10

        # Elements follow the tuple pattern (DISPLAY_STRING, id)
        self.full_elements = []
        self.page_elements = []

        self.actual_title = 'Main Menu'
        self.subtitle = "Options"
        self.states = []
        # this just so happens to work in my favor!
        self.main_menu()

    def main_menu(self):
        '''Set everything necessary for the main menu'''
        if len(self.states) == 0:
            elements = [
                MenuElement('View Suggested Songs', 'suggested'),
                MenuElement('Browse Albums', 'album'),
                MenuElement('Browse Artists', 'artist'),
                MenuElement('Browse Playlists', 'playlist'),
                MenuElement('Browse Radios', 'radio'),
                MenuElement('Browse Songs', 'song'),
                MenuElement('Connect to DJs', 'dj'),
                MenuElement('Options', 'options'),
                MenuElement('Exit', 'exit')]

            main_state = State("Main Menu", "Options", elements)
            main_state.id = 'main'

            self.push_state(main_state)
            return

        # Delete all other states
        self.states[1:] = []
        self.assign_state(self.states[0])

    def options_menu(self):
        '''Pushses options menu to top of stack'''
        elements = [
            MenuElement('Background color', 'back', 'Gray'),
            MenuElement('Text color', 'back', 'White'),
            MenuElement('Highlight color', 'back', 'White'),
            MenuElement('Number of radio tracks to pull', 'back', '25'),
            MenuElement('Port for DJ Notifications', 'back', '8080'),
            MenuElement('Allow DJ to control playback', 'back', 'No'),
            MenuElement('Back','back')]
        title = 'Options Menu'
        subtitle = 'Options'
        options_state = State(title, subtitle, elements)
        options_state.id = 'options'

        self.push_state(options_state)


    def push_state(self, state):
        '''Pushes a state on the StateStack'''
        self.states.append(state)
        self.assign_state(state)

    def pop_state(self):
        '''Pops a state off of the StateStack, then peeks'''
        if len(self.states) == 1:
            return

        self.states.pop()
        self.assign_state(self.states[-1])

    def assign_state(self, state):
        self.actual_title = state.title
        self.subtitle = state.subtitle
        self.set_options(state.elements)
        self.set_page(0)

    def current_state_is(self, identifier):
        return self.states[-1].id == identifier


    def get_selected_element(self):
        return self.page_elements[self.selected_element]

    def get_seed_type(self):
        if self.current_state_is('songs') or self.current_state_is('artists') or self.current_state_is('albums'):
            return self.state.lower()
        return ''

    def adjust_selection(self, amount):
        """Adjusts the position of the selection cursor in the menu"""
        self.selected_element += amount
        self.selected_element = self.selected_element % len(self.page_elements)

    def change_page(self, value):
        '''Add `value` to the page_number, constrain it, then set page'''
        new_page = self.constrain_page_number(self.page_number + value)
        self.set_page(new_page)

    def set_page(self, page):
        '''Set the page to a specific page number'''
        self.selected_element = 0
        self.page_number = page
        self.page_elements = self.full_elements[self.page_number]

        # Handle Page Number
        self.title = self.actual_title
        if len(self.full_elements) > 1:
            self.title = self.title + ' (Page {0} of {1})'.format(self.page_number+1, len(self.full_elements))

        # If this isn't the main menu, make sure that we have 'BACK' available
        if not self.current_state_is('main') and self.page_elements[-1].id != 'back':
            self.page_elements.append(MenuElement('Back','back'))

    def handle_execute(self):
        '''State Machine'''
        if self.current_state_is('main'):
            return self.page_elements[self.selected_element].id

        # First and foremost, go BACK if the element says to do so
        if self.page_elements[self.selected_element].id == 'back':
            return 'back'

        # Look up Albums by an artist
        if self.current_state_is('artists'):
            return 'artist_albums {0}'.format(self.get_selected_element().id)

        # Look up Songs in an album
        if self.current_state_is('albums'):
            return 'album_songs {0}'.format(self.get_selected_element().id)

        if self.current_state_is('playlists'):
            return 'playlist_songs {0}'.format(self.get_selected_element().id)

        # otherwise, play!
        return "play {0} {1}".format(\
            self.states[-1].id[:-1],\
            self.get_selected_element().id)

    def set_options(self, new_options):
        '''Splits the elements up into sublists for pages'''
        self.full_elements = [new_options[x:x+self.capacity] \
            for x in range(0, len(new_options), self.capacity)]
        self.set_page(0)

    def constrain_page_number(self, new_page_number):
        return max(min(new_page_number, len(self.full_elements)-1), 0)
