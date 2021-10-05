from settings import *
import pygame as pg
import random

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

class Consumable(Item):
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
        for i in range(0,len(game.player.images)):
            for j in range(0,len(game.player.images[i])):
                game.player.images[i][j].blit(self.images[i][j], (0,0))

    def unequip_effect(self, game):
        walk_down_img = [path.join(img_folder, 'f1.png'), path.join(img_folder, 'f2.png'), path.join(img_folder, 'f3.png'), path.join(img_folder, 'f4.png')]
        walk_up_img = [path.join(img_folder, 'b1.png'), path.join(img_folder, 'b2.png'), path.join(img_folder, 'b3.png'), path.join(img_folder, 'b4.png')]
        walk_left_img = [path.join(img_folder, 'l1.png'), path.join(img_folder, 'l2.png'), path.join(img_folder, 'l3.png'), path.join(img_folder, 'l4.png')]
        walk_right_img = [path.join(img_folder, 'r1.png'), path.join(img_folder, 'r2.png'), path.join(img_folder, 'r3.png'), path.join(img_folder, 'r4.png')]
        npc_down = [pg.image.load(walk_down_img[0]), pg.image.load(walk_down_img[1]), pg.image.load(walk_down_img[2]), pg.image.load(walk_down_img[3])]
        npc_up = [pg.image.load(walk_up_img[0]), pg.image.load(walk_up_img[1]), pg.image.load(walk_up_img[2]), pg.image.load(walk_up_img[3])]
        npc_left = [pg.image.load(walk_left_img[0]), pg.image.load(walk_left_img[1]), pg.image.load(walk_left_img[2]), pg.image.load(walk_left_img[3])]
        npc_right = [pg.image.load(walk_right_img[0]), pg.image.load(walk_right_img[1]), pg.image.load(walk_right_img[2]), pg.image.load(walk_right_img[3])]
        game.player.images = [npc_down, npc_up, npc_left, npc_right]

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

class InvisibilityCloak(Armor):
    def __init__(self):
        super().__init__()
        self.name = 'Invisibility Cloak'

    def equip_effect(self, game):
        game.player.invisible = True
        for img_list in game.player.images:
            for img in img_list:
                img.set_alpha(100)

    def unequip_effect(self, game):
        game.player.invisible = False
        for img_list in game.player.images:
            for img in img_list:
                img.set_alpha(255)

class Cauldron(Item):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def get_details(self):
        return {}

class PumpkinJuice(Consumable):
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


wand = Wand('Larch', 'Dragon Heartstring', '11 inches', 'Swishy')
cauldron = Cauldron('Black Cauldron')
cloak = InvisibilityCloak()
broom = Broom('Nimbus 2000')
juice = PumpkinJuice()
test_inventory = [cauldron, cloak, broom]
print(isinstance(cloak, Equippable))
