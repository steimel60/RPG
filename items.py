from settings import *
import pygame as pg
import random

class Item():
    def __init__(self):
        self.type = '' #Ex) Wand, Card, Cloak
        self.name = '' #Specific Item name Ex) Larch Wand
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
        super().__init__()
        #Wand Details
        self.wood = wood
        self.core = core
        self.length = length
        self.flex = flex
        self.type = 'Wand'
        self.maker = maker
        self.name = f'{self.wood} {self.type}'
        #Wand Images
        wand_down_img = [path.join(img_folder, 'wand_f1.png'), path.join(img_folder, 'wand_f2.png'), path.join(img_folder, 'wand_f3.png'), path.join(img_folder, 'wand_f4.png')]
        wand_up_img = [path.join(img_folder, 'wand_b1.png'), path.join(img_folder, 'wand_b2.png'), path.join(img_folder, 'wand_b3.png'), path.join(img_folder, 'wand_b4.png')]
        wand_left_img = [path.join(img_folder, 'wand_l1.png'), path.join(img_folder, 'wand_l2.png'), path.join(img_folder, 'wand_l3.png'), path.join(img_folder, 'wand_l4.png')]
        wand_right_img = [path.join(img_folder, 'wand_r1.png'), path.join(img_folder, 'wand_r2.png'), path.join(img_folder, 'wand_r3.png'), path.join(img_folder, 'wand_r4.png')]
        wand_down = [pg.image.load(wand_down_img[0]), pg.image.load(wand_down_img[1]), pg.image.load(wand_down_img[2]), pg.image.load(wand_down_img[3])]
        wand_up = [pg.image.load(wand_up_img[0]), pg.image.load(wand_up_img[1]), pg.image.load(wand_up_img[2]), pg.image.load(wand_up_img[3])]
        wand_left = [pg.image.load(wand_left_img[0]), pg.image.load(wand_left_img[1]), pg.image.load(wand_left_img[2]), pg.image.load(wand_left_img[3])]
        wand_right = [pg.image.load(wand_right_img[0]), pg.image.load(wand_right_img[1]), pg.image.load(wand_right_img[2]), pg.image.load(wand_right_img[3])]
        self.images = [wand_down, wand_up, wand_left, wand_right]
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
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = self.get_image()

    def get_details(self):
        return {}

    def get_image(self):
        pass

    def equip_effect(self, game):
        pass

    def unequip_effect(self, game):
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
cauldron = Cauldron('Black Cauldron')
cloak = InvisibilityCloak()
broom = Broom('Nimbus 2000')
juice = PumpkinJuice()
test_inventory = [cauldron, cloak, broom, juice]
