class Item():
    def __init__(self):
        self.type = '' #Ex) Wand, Card, Cloak
        self.name = '' #Specific Item name Ex) Larch Wand
        self.details = {} #Dict of Item details
        self.icon = None #Inventory icon
        self.image = None #Specific item image

    def print_details(self):
        details = self.get_details()
        for detail in details:
            print(f'{detail}: {details[detail]}')

class Wand(Item):
    def __init__(self, wood, core, length, flex, maker=None):
        #Wand Details
        self.wood = wood
        self.core = core
        self.length = length
        self.flex = flex
        self.type = 'Wand'
        self.maker = maker
        self.name = f'{self.wood} {self.type}'


    def change_wood(self):
        self.wood = 'Elder'
        self.name = f'{self.wood} {self.type}'

    def get_details(self):
        details = {
            'Wood' : self.wood,
            'Core' : self.core,
            'Length' : self.length,
            'Flexibility' : self.flex,
            'Maker' : self.maker
        }
        return details

wand = Wand('Larch', 'Dragon Heartstring', '11 inches', 'Swishy')
wand.print_details()
print(wand.name)
wand.change_wood()
print('\n')
wand.print_details()
print(wand.name)
