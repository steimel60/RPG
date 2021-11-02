from items import *

class HogwartsCloak(Cloak):
    def __init__(self, house):
        self.folder_name = 'Hogwarts Cloak'
        self.name = f'{house.name} Cloak'
        self.house = house
        self.color_dict = {
                'Transparent': {'Template':(255,255,255), 'Current':(0,0,0,0)},
                'Main': {'Template':(0,0,0), 'Current':(0,0,0)},
                'Accent': {'Template':(237,28,36), 'Current':house.color},
                'Wrinkle': {'Template':(127,127,127), 'Current':(40,40,40)}
                }
        super().__init__()
        self.initialize_color()

class BasicPants(Pants):
    def __init__(self):
        self.folder_name = 'Basic'
        self.name = 'Old Pants'
        self.color_dict = {
                'Transparent': {'Template':(255,255,255), 'Current':(0,0,0,0)},
                'Main': {'Template':(0,0,255), 'Current':(40,40,40)}
                }
        super().__init__()
        self.initialize_color()

class HogwartsTie(Shirt):
    def __init__(self, house):
        self.folder_name = 'Hogwarts Tie'
        self.name = f'{house.name} Shirt and Tie'
        self.color_dict = {
                'Transparent': {'Template':(255,255,255), 'Current':(0,0,0,0)},
                'Main': {'Template':(255,0,255), 'Current':(255,255,255)},
                'Tie Main': {'Template':(255,0,0), 'Current':house.color},
                'Tie Accent': {'Template':(255,255,0), 'Current':house.secondary_color}
                }
        super().__init__()
        self.initialize_color()
