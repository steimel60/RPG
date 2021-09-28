import pygame as pg
from settings import *

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
    def run(self):
        pass
