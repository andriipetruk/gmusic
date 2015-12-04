class State(object):
    def __init__(self):
        self.state = ""
        self.title = ""
        self.subtitle = ""
        self.selected_element = 0
        self.page_number = 0

        # Elements follow the tuple pattern (DISPLAY_STRING, id)
        self.full_elements = []
        self.state_aliases = [('Artists','artist'), ('Albums','album'), \
            ('Radios', 'radio'), ('Songs', 'song'), ('DJs', 'dj'), \
            ('Options', 'options'), ('Exit', 'exit')]
        self.page_elements = []

        # this just so happens to work in my favor!
        self.main_menu()

    def main_menu(self):
        '''Set everything necessary for the main menu'''
        self.full_elements = [self.state_aliases]
        self.page_elements = self.state_aliases
        self.state = "main"
        self.title = "Main Page"
        self.subtitle = "Options"
        self.selected_element = 0

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
        self.title = self.state
        if len(self.full_elements) > 1:
            self.title = self.title + ' (Page {0} of {1})'.format(self.page_number+1, len(self.full_elements))

        # If this isn't the main menu, make sure that we have 'BACK' available
        if self.state != 'main' and self.page_elements[-1][0] != 'Back':
            self.page_elements.append(('Back','back'))

    def handle_execute(self):
        '''State Machine'''
        if self.state == 'main':
            return self.page_elements[self.selected_element][1]

        # Check to see if we're trying to go back to main menu
        if self.page_elements[self.selected_element][0] == 'Back':
            return 'back'

        if self.state == 'Artists' or self.state == 'Albums':
            return 'song {0}'.format(self.page_elements[self.selected_element][0])

        state = [alias[1] for alias in self.state_aliases if self.state == alias[0]][0]
        return "play {0} {1}".format(\
            state,\
            self.page_elements[self.selected_element][1])

    def set_options(self, new_options, capacity):
        '''Splits the elements up into sublists for pages'''
        self.full_elements = [new_options[x:x+capacity] \
            for x in range(0, len(new_options), capacity)]
        self.change_page(0)

    def constrain_page_number(self, new_page_number):
        return max(min(new_page_number, len(self.full_elements)-1), 0)
