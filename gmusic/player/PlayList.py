import random

class PlayList:
    '''Simple object which maintains track NIDs and location'''

    def __init__(self):
        self.contents = []
        self.index = 0
        self.random = False

    def load(self, new_contents):
        self.index = 0
        self.contents = new_contents

    def toggle_random(self):
        toggled = True + self.random
        self.random = toggled % 2

    def next(self):
        if self.random:
            return self.next_shuffle()
        return self.next_direct()

    def next_direct(self):
        '''Increments the index, but loops back if overflow'''
        self.index = (self.index + 1) % len(self.contents)
        return self.contents[self.index]

    def previous(self):
        '''Decrements the index, but loops back if overflow'''
        self.index = (self.index - 1) % len(self.contents)
        return self.contents[self.index]

    def next_shuffle(self):
        '''Get a random element from the contents'''
        self.index = random.randint(0, len(self.contents)-1)
        return self.contents[self.index]
