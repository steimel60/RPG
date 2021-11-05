from items import *
from houses import *
import random
from settings import skin_colors

Special_NPCs = {
'DJ' : {'Name':'DJ',
        'House':RavenclawHouse,
        'Cloak' : HogwartsCloak(RavenclawHouse),
        'Shirt' : HogwartsTie(RavenclawHouse),
        'Pants' : BasicPants(),
        'Skin ID' : 2,
        'Hair ID' : 3,
        'Hair Color' : 0,
        'Pet':'Owl'},
'Loren' : {'Name':'Loren',
        'House':RavenclawHouse,
        'Cloak' : HogwartsCloak(RavenclawHouse),
        'Shirt' : HogwartsTie(RavenclawHouse),
        'Pants' : BasicPants(),
        'Skin ID' : 0,
        'Hair ID' : 1,
        'Hair Color' : 1,
        'Pet':'Mouse'},
'Logan' : {'Name':'Logan',
        'House':RavenclawHouse,
        'Cloak' : HogwartsCloak(RavenclawHouse),
        'Shirt' : HogwartsTie(RavenclawHouse),
        'Pants' : BasicPants(),
        'Skin ID' : 0,
        'Hair ID' : 1,
        'Hair Color' : 0,
        'Pet':'Fox'},
'Wanda' : {'Name':'Wanda',
        'House':HufflepuffHouse,
        'Cloak' : HogwartsCloak(HufflepuffHouse),
        'Shirt' : HogwartsTie(HufflepuffHouse),
        'Pants' : BasicPants(),
        'Skin ID' : 0,
        'Hair ID' : 2,
        'Hair Color' : 3,
        'Pet':'Fox'},
'Dr. Booksy' : {'Name':'Dr. Booksy',
        'House':HufflepuffHouse,
        'Cloak' : HogwartsCloak(HufflepuffHouse),
        'Shirt' : HogwartsTie(HufflepuffHouse),
        'Pants' : BasicPants(),
        'Skin ID' : 1,
        'Hair ID' : 3,
        'Hair Color' : 2,
        'Pet':'Fox'}
}

class RandomNPCDataGenerator():
    def __init__(self):
        self.name = self.generate_name()
        self.house = self.generate_house()
        self.cloak = HogwartsCloak(self.house)
        self.shirt = HogwartsTie(self.house)
        self.pants =  BasicPants()
        self.skin_id = self.generate_skin_id()
        self.hair_id = self.generate_hair_style()
        self.hair_color = self.generate_hair_color()
        self.data_dict = {
                'Name' : self.name,
                'House' : self.house,
                'Cloak' : self.cloak,
                'Shirt' : self.shirt,
                'Pants' : self.pants,
                'Skin ID' : self.skin_id,
                'Hair ID' : self.hair_id,
                'Hair Color' : self.hair_color
        }

    def generate_name(self):
        names = ['Bill', 'Bob', 'Lola', 'Tito']
        return random.choice(names)

    def generate_house(self):
        return random.choice([GryffindorHouse,SlytherinHouse,HufflepuffHouse,RavenclawHouse])

    def generate_skin_id(self):
        return random.choice([x for x in range(0,len([skin_colors]))])

    def generate_hair_style(self):
        return random.choice([x for x in range(0,4)])

    def generate_hair_color(self):
        return random.choice([x for x in range(0,4)])

npcData = RandomNPCDataGenerator()
print(npcData.name)
print(npcData.house)
print(npcData.skin_id)
