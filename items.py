from settings import *
import pygame as pg
import random
from houses import GryffindorHouse, SlytherinHouse, HufflepuffHouse, RavenclawHouse

class Item():
    def __init__(self):
        #self.type = '' #Ex) Wand, Card, Cloak
        #self.name = '' #Specific Item name Ex) Larch Wand
        self.details = {} #Dict of Item details
        self.icon = None #Inventory icon
        self.actions = ['Details','Destroy']
        self.action_dict = {}

    def print_details(self):
        details = self.get_details()
        for detail in details:
            print(f'{detail}: {details[detail]}')

class Equippable(Item):
    '''
    Equippables are items that may be equipped to a character
    '''
    def __init__(self):
        super().__init__()
        self.actions += ['Equip']

    def equip_effect(self, game):
        pass

    def unequip_effect(self, game):
        pass

class Wearable(Equippable):
    '''
    Wearables are Equippables that have images
    '''
    def __init__(self):
        super().__init__()
        #Images
        self.image = pg.Surface((TILESIZE,TILESIZE))
        front_file_names = ['f1.png','f2.png','f3.png','f4.png']
        back_file_names = ['b1.png','b2.png','b3.png','b4.png']
        left_file_names = ['l1.png','l2.png','l3.png','l4.png']
        right_file_names = ['r1.png','r2.png','r3.png','r4.png']
        down_images_paths = [path.join(self.image_folder, filename) for filename in front_file_names]
        up_images_paths = [path.join(self.image_folder, filename) for filename in back_file_names]
        left_images_paths = [path.join(self.image_folder, filename) for filename in left_file_names]
        right_images_paths = [path.join(self.image_folder, filename) for filename in right_file_names]
        self.loaded_down_images = [pg.image.load(img) for img in down_images_paths]
        self.loaded_up_images = [pg.image.load(img) for img in up_images_paths]
        self.loaded_left_images = [pg.image.load(img) for img in left_images_paths]
        self.loaded_right_images = [pg.image.load(img) for img in right_images_paths]
        self.images = [self.loaded_down_images, self.loaded_up_images, self.loaded_left_images, self.loaded_right_images]

    def initialize_color(self):
        for layer in self.color_dict:
            template_color = self.color_dict[layer]['Template']
            new_color = self.color_dict[layer]['Current']
            for img_list in self.images:
                for img in img_list:
                    img_arr = pg.PixelArray(img)
                    img_arr.replace (template_color, new_color)
                    del img_arr

class Consumable(Item):
    def __init__(self):
        super().__init__()

class Food(Consumable):
    def __init__(self):
        super().__init__()
        self.actions += ['Eat']

class Drink(Consumable):
    def __init__(self):
        super().__init__()
        self.actions += ['Drink']

class Armor(Wearable):
    def __init__(self):
        super().__init__()

class Pants(Armor):
    def __init__(self):
        pants_folder = path.join(clothes_folder, 'Pants')
        self.image_folder = path.join(pants_folder, self.folder_name)
        super().__init__()

    def equip_effect(self, game):
        game.player.pants = self

    def unequip_effect(self, game):
        game.player.pants = None

class Shirt(Armor):
    def __init__(self):
        shirts_folder = path.join(clothes_folder, 'Shirts')
        self.image_folder = path.join(shirts_folder, self.folder_name)
        super().__init__()

    def equip_effect(self, game):
        game.player.shirt = self

    def unequip_effect(self, game):
        game.player.shirt = None

class Book(Item):
    def __init__(self):
        super().__init__()

class SpellBook(Item):
    def __init__(self):
        super().__init__()

class Interactable(Item):
    def __init__(self):
        super().__init__()

class LockedItem(Interactable):
    def __init__(self):
        super().__init__()

class Wand(Wearable):
    def __init__(self, wood, core, length, flex, maker=None):
        self.image_folder = path.join(img_folder, 'Wands')
        super().__init__()
        #Wand Details
        self.wood = wood
        self.core = core
        self.length = length
        self.flex = flex
        self.type = 'Wand'
        self.maker = maker
        self.name = f'{self.wood} {self.type}'
        self.change_color()

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

    def equip_effect(self, game):
        game.player.wand = self

    def unequip_effect(self, game):
        game.player.wand = None

    def change_color(self):
        new_color = random.choice([(222,184,135),(244,164,96),(139,69,19)])
        for img_list in self.images:
            for img in img_list:
                img_arr = pg.PixelArray(img)
                img_arr.replace (BLACK, new_color)
                del img_arr

class Broom(Equippable):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_details(self):
        return {}

    def equip_effect(self, game):
        game.player.speed = BROOM_SPEED

    def unequip_effect(self, game):
        game.player.speed = WALK_SPEED

class Cloak(Armor):
    def __init__(self):
        cloaks_folder = path.join(clothes_folder, 'Cloaks')
        self.image_folder = path.join(cloaks_folder, self.folder_name)
        super().__init__()

    def get_details(self):
        return {}

    def equip_effect(self, game):
        game.player.cloak = self

    def unequip_effect(self, game):
        game.player.cloak = None

    def draw(self):
        pass

    def update(self):
        pass

class InvisibilityCloak(Equippable):
    def __init__(self):
        super().__init__()
        self.name = 'Invisibility Cloak'

    def equip_effect(self, game):
        game.player.invisible = True
        for img_list in game.player.images:
            for img in img_list:
                img.set_alpha(100)
        #Change equipped item images
        for item in [game.player.hat, game.player.shirt, game.player.cloak, game.player.wand]:
            if item != None:
                for img_list in item.images:
                    for img in img_list:
                        img.set_alpha(100)

    def unequip_effect(self, game):
        game.player.invisible = False
        for img_list in game.player.images:
            for img in img_list:
                img.set_alpha(255)
        #Change equipped item images
        for item in [game.player.hat, game.player.shirt, game.player.cloak, game.player.wand]:
            if item != None:
                for img_list in item.images:
                    for img in img_list:
                        img.set_alpha(255)

class Cauldron(Item):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def get_details(self):
        return {}

class PumpkinJuice(Drink):
    def __init__(self):
        super().__init__()
        self.name = 'Pumpkin Juice'
    def get_details(self):
        return {}

class ChocolateFrogCard(Item):
    def __init__(self, name):
        super().__init__()
        self.name = f'{name} Card'
    def get_details(self):
        return {}

class BasicSpellBook(SpellBook):
    def __init__(self):
        super().__init__()

class SpellScroll(SpellBook):
    def __init__(self, spell):
        super().__init__()
        self.spell = spell
        self.name = f"{self.spell.name} Scroll"
        self.actions += ['Read', 'Learn Spell']

    def learn_spell(self, game):
        game.SpellHandler.learn_spell(self.spell)
        print(f"You now know how to cast {self.spell.name}!")

class Spell():
    def __init__(self):
        pass

class Alohamora(Spell):
    def __init__(self):
        super().__init__()
        self.name = 'Alohamora'
        self.level = 1

    def cast(self, item):
        if isinstance(item, LockedItem):
            if item.locked:
                item.locked = False
                item.update()

wand = Wand('Larch', 'Dragon Heartstring', '11 inches', 'Swishy')
wand2 = Wand('Elder', 'Unicorn Hair', '10 inches', 'Springy')
cauldron = Cauldron('Black Cauldron')
cloak = InvisibilityCloak()
from cloaks import HogwartsCloak, BasicPants, HogwartsTie
broom = Broom('Nimbus 2000')
juice = PumpkinJuice()
test_inventory = [wand, wand2, cauldron, cloak, broom, juice]
print(type(wand))
