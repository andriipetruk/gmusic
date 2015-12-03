class State(object):
    def __init__(self):
        self.state = ""
        self.title = "Main Page"
        self.subtitle = "Options"
        self.selected_element = 0
        self.page_number = 0
        self.full_elements = []
        self.page_elements = ['Artists','Albums','Radios','Songs','DJs','Options', 'Exit']

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
