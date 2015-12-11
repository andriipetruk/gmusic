class State:
    '''Data structure which houses all information about a State'''

    def __init__(self, title, subtitle, elements, data=None):
        self.title = title
        self.subtitle = subtitle
        self.elements = elements
        self.data = data
        self.id = subtitle.lower()
