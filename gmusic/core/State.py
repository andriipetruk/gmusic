class State(object):
    def __init__(self):
        self.state = ""
        self.title = "Main Page"
        self.subtitle = "Options"
        self.selected_element = 0
        self.page_number = 0

        # Elements follow the tuple pattern (DISPLAY_STRING, id)
        self.full_elements = []
        self.page_elements = [('Artists',None), ('Albums',None), \
            ('Radios', None), ('Songs', None), ('DJs', None), \
            ('Options', None), ('Exit', None)]

    def adjust_selection(self, amount):
        """Adjusts the position of the selection cursor in the menu"""
        self.selected_element += amount
        if self.selected_element > len(self.page_elements):
            self.change_page(1)
        if self.selected_element < 0:
            self.change_page(-1)
        self.selected_element = self.selected_element % len(self.page_elements)

    def change_page(self, page):
        pass

    def handle_execute(self):
        if self.page_elements[self.selected_element][0] == 'Artists':
            return 'artist'
        if self.page_elements[self.selected_element][0] == 'Albums':
            return 'album'
        if self.page_elements[self.selected_element][0] == 'Songs':
            return 'song'
        if self.page_elements[self.selected_element][0] == 'Radios':
            return 'radio'
        return ''

    def set_options(self, new_options, pattern):
        self.page_elements = new_options


'''
The CursedMenu uses this to keep track of where the user is.

states:
    main - Main menu
    options - Options menu
    playlists - List of playlists
    playlist - A specific playlist
    radios - List of radios
    radio - A specfic radio
    search - Search menu
'''
