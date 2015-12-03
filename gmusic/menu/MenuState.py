class MenuState(object):
    def __init__(self):
        self.state = ""
        self.selected_element = 0
        self.page_number = 0

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
