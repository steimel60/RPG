import pygame as pg
from settings import *
from items import *
import random

shopList = []
def get_shop(shop_id):
    if shop_id == 'wandshop1':
        return WandShop()
class Shop():
    def __init__(self, game, x, y, h, w, shop_id):
        self.game = game
        self.shop_id = shop_id
        self.shop = get_shop(shop_id)
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def get_shop_gui(self):
        return ShopGUI(self.game, self.shop)

    def check_interactions(self):
        self.game.shop = self
        print(f'Opening Shop {self.shop}')
        self.game.current_state = 'shop'

    def update(self):
        #self.gui.update()
        pass

class WandShop():
    def __init__(self):
        self.tiled_id = 'wandshop1'
        self.name = "Wanda's Wand Shop"
        self.clerk = 'Wanda'
        self.items = {
                    'Random Wand':
                            {'cost':(0,1,15)},
                    'Rare Wand':
                            {'cost':(10,0,0)}
                            }
    def has_prereqs(self):
        return True
    def check_prereqs(self):
        pass
    def check_for_special_buy(self, item):
        return True
    def special_buy(self, state, item):
        state.text = "Let's see... the wand chooses the wizard you know"
        state.draw()
        self.wait_for_key_up(state)
        self.find_wand(state)

    def wait_for_key_up(self, state):
        temp = state.dialog_state
        state.dialog_state = 'waiting'
        hit_space = False
        while not hit_space:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    #next
                    if event.key == pg.K_SPACE:
                        hit_space = True
        state.dialog_state = temp

    def get_random_wand(self):
        woods = ['Larch', 'Cherry', 'Elder', 'Oak', 'Willow', 'Alder', 'Blackthorn']
        x = 7
        lengths = []
        while x <= 13:
            lengths.append(x)
            x += .5
        cores = ['Dragon Heart String', 'Unicorn Hair', 'Pheonix Feather']
        flexes = ['Swishy', 'Pliant', 'Rigid']
        wood = random.choice(woods)
        length = random.choice(lengths)
        core = random.choice(cores)
        flex = random.choice(flexes)
        return wood, core, length, flex

    def find_wand(self, state):
        wand_found = False
        try_count = 0
        while not wand_found:
            wood, core, length, flex = self.get_random_wand()
            state.text = f"Hmm.. {wood}.."
            state.draw()
            self.wait_for_key_up(state)
            state.text = f"{core}.. {length} inches.. {flex}"
            state.draw()
            self.wait_for_key_up(state)
            state.text = f"Yes, yes, give this a try!"
            state.draw()
            self.wait_for_key_up(state)
            wand_found = self.try_wand(try_count)
            if wand_found:
                state.text = f"Yes! That is the one!"
                state.purchased_item = Wand(wood, core, length, flex)
                state.draw()
                self.wait_for_key_up(state)
            else:
                state.text = f"Oh no, that won't work."
                state.draw()
                self.wait_for_key_up(state)
                try_count += 1

    def try_wand(self, try_count):
        if try_count > 3:
            return True
        else:
            return random.choice([True, False, False])

    def run(self):
        pass
