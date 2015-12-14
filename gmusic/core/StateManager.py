from gmusic.model.MenuElement import MenuElement
from gmusic.model.State import State
from gmusic.model.commands import *

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
                MenuElement('View Suggested Songs', id='', command='Suggested'),
                MenuElement('Browse Albums', id='', command='Album'),
                MenuElement('Browse Artists', id='', command='Artist'),
                MenuElement('Browse Playlists', id='', command='Playlist'),
                MenuElement('Browse Radios', id='', command='Radio'),
                MenuElement('Browse Songs', id='', command='Song'),
                MenuElement('Connect to DJs', id='', command='Main'),
                MenuElement('Options', id='', command='Options'),
                MenuElement('Exit', id='', command='Exit')]

            main_state = State("Main Menu", "Options", elements)
            main_state.id = 'main'

            self.push_state(main_state)
            return

        # Delete all other states
        self.states[1:] = []
        self.assign_state(self.states[0])

    def options_menu(self):
        '''Pushses options menu to top of stack'''


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


    def get_selected_element(self):
        return self.page_elements[self.selected_element]

    def current_state_is(self, identifier):
        return self.states[-1].id == identifier

    def get_seed_type(self):
        if self.current_state_is('songs') or self.current_state_is('artists') or self.current_state_is('albums'):
            return self.states[-1].id[:-1]
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
        if not self.current_state_is('main') and self.page_elements[-1].command != 'Back':
            self.page_elements.append(MenuElement('Back','','Back'))


    def handle_execute(self):
        '''State Machine'''
        element = self.get_selected_element()
        return (element.command, {'id': element.id})


    def set_options(self, new_options):
        '''Splits the elements up into sublists for pages'''
        self.full_elements = [new_options[x:x+self.capacity] \
            for x in range(0, len(new_options), self.capacity)]
        self.set_page(0)

    def constrain_page_number(self, new_page_number):
        return max(min(new_page_number, len(self.full_elements)-1), 0)
