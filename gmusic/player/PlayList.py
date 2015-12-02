import random

class PlayList:
    '''Simple object which maintains track nids and location'''

    def __init__(self):
        self.contents = []
        self.index = 0

    def load(self, new_contents):
        self.index = 0
        self.contents = new_contents

    def next(self):
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
