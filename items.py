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

    def is_equippable(self):
        return isinstance(self,Equippable)

    def is_armor(self):
        return isinstance(self,Armor)

class Equippable(Item):
    def __init__(self):
        super().__init__()

class Armor(Equippable):
    def __init__(self):
        super().__init__()

class Wand(Equippable):
    def __init__(self, wood, core, length, flex, maker=None):
        super().__init__()
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

class Cloak(Armor):
    def __init__(self):
        super().__init__()
    def get_details(self):
        return {}

class Cauldron(Item):
    def __init__(self, maker=None):
        super().__init__()
    def get_details(self):
        return {}

wand = Wand('Larch', 'Dragon Heartstring', '11 inches', 'Swishy')
cauldron = Cauldron()
cloak = Cloak()
print('Wand Print Statements')
wand.print_details()
print(f'Wand Name: {wand.name}')
print(f'Item Instance: {isinstance(wand,Item)}')
print(f'Equippable Instance: {isinstance(wand,Equippable)}')
print(f'Armor Instance: {isinstance(wand,Armor)}')
print(f'Wand Instance: {isinstance(wand,Wand)}')
print(f'Cauldron Instance: {isinstance(wand,Cauldron)}')
print('\n')
print('Cauldron Print Statements')
print(f'Item Instance: {isinstance(cauldron,Item)}')
print(f'Equippable Instance: {isinstance(cauldron,Equippable)}')
print(f'Armor Instance: {isinstance(cauldron,Armor)}')
print(f'Wand Instance: {isinstance(cauldron,Wand)}')
print(f'Cauldron Instance: {isinstance(cauldron,Cauldron)}')
cauldron.print_details()
print('\n')
print('Cloak Print Statements')
print(f'Item Instance: {isinstance(cloak,Item)}')
print(f'Equippable Instance: {isinstance(cloak,Equippable)}')
print(f'Armor Instance: {isinstance(cloak,Armor)}')
print(f'Wand Instance: {isinstance(cloak,Wand)}')
print(f'Cauldron Instance: {isinstance(cloak,Cauldron)}')
cloak.print_details()
