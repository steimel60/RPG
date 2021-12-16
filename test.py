class thing1():
    def __init__(self):
        self.name = 'item1'

    def print(self):
        print('Item 1 print')

    def super_print(self):
        print('I am a thing1')

class thing2(thing1):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def print(self):
        print(f'My name is {self.name}')
        self.super_print()

thing = thing2('car')
thing.print()
thing.super_print()
