#import pygame as pg
#from settings import *
from menu_states import *

class GameplayState():
    def __init__(self, game):
        self.game = game

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.game.player.check_for_interactions()
                if event.key == pg.K_i:
                    self.game.current_state = 'menu'
                    self.game.STATE_DICT['menu'].open_inventory()
                if event.key == pg.K_m:
                    self.game.current_state = 'menu'
                if event.key == pg.K_g:
                    for gate in self.game.gates:
                        gate.locked = False
            keys = pg.key.get_pressed()
                #if keys[pg.K_c]:
                    #skin_select(self)

    def draw(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        self.game.draw_grid()
        for sprite in self.game.all_sprites:
            sprite.draw(self.game)
        self.game.screen.blit(self.game.textbox.image, (20,500))
        pg.display.flip()

    def update(self):
        self.game.all_sprites.update()
        self.game.textbox.update()
        self.game.camera.update(self.game.player)
        self.game.check_level()

class ShopState():
    def __init__(self, game):
        self.game = game
        self.shop = self.game.shop
        self.selection = False
        self.selectionCount = 0
        self.menu_image = pg.Surface((300,600))
        self.menu_image.fill(WHITE)
        self.width = 224
        self.items = None
        self.purchased_item = None
        self.dialog_state = 'dialog'
        self.ans = 'yes'
        #Text data
        self.text = None
        self.fontLocs = []
        self.font = pg.font.Font('freesansbold.ttf', 12)

    def get_shop(self):
        self.shop = self.game.shop

    def events(self):
        if self.dialog_state == 'dialog':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.quit()
                if event.type == pg.KEYUP:
                    #close
                    if event.key == pg.K_c:
                        self.close_shop()
                    #scroll down
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if not self.selection:
                            self.selection = True
                            self.selectionCount -= 1
                        self.selectionCount += 1
                        if self.selectionCount > len(self.items)-1:
                            self.selectionCount=0
                    #scroll up
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if not self.selection:
                            self.selection = True
                            self.selectionCount += 1
                        self.selectionCount -= 1
                        if self.selectionCount < 0:
                            self.selectionCount = len(self.items)-1
                    #select
                    if event.key == pg.K_SPACE:
                        if self.selection:
                            self.buy()
                        else:
                            self.selection = True
        if self.dialog_state == 'question':
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN or event.key == pg.K_s or event.key == pg.K_UP or event.key == pg.K_w:
                        if self.ans == 'yes':
                            self.ans = 'no'
                        else:
                            self.ans = 'yes'
                        #select
                    if event.key == pg.K_SPACE:
                        self.answer()

    def get_items(self):
        self.items = {item:self.shop.shop.items[item]['cost'] for item in self.shop.shop.items}

    def get_shop_dialog(self):
        if self.text == None:
            self.text = f'Welcome to {self.shop.shop.name}!'

    def draw(self):
        self.draw_shop_menu()
        self.draw_text()
        self.draw_selection_box()
        self.game.textbox.draw_box()
        text = self.text
        if self.dialog_state == 'dialog':
            self.game.textbox.draw_dialogue(self.shop.shop.clerk, text)
        elif self.dialog_state == 'question':
            self.game.textbox.yes_no_question(self.shop.shop.clerk, text, self.ans)
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.menu_image, (800,30))
        pg.display.flip()

    def draw_shop_menu(self):
        self.menu_image.fill(WHITE)

    def draw_text(self):
        galleons = self.game.player.galleons
        sickles = self.game.player.sickles
        knuts = self.game.player.knuts
        font = self.font
        bigfont = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        blitLoc = [10,0]
        Locs = []
        #Blit Money
        shopLabel = self.shop.shop.name
        text = bigfont.render(shopLabel, True, BLACK, WHITE)
        size = bigfont.size(shopLabel)
        centerX = size[0]//2
        self.menu_image.blit(text, (self.width//2-centerX,0))
        blitLoc[1] += size[1]
        moneyLabel = "Your Money"
        text = font.render(moneyLabel, True, BLACK, WHITE)
        size = font.size(moneyLabel)
        centerX = size[0]//2
        self.menu_image.blit(text, (0,blitLoc[1]))
        blitLoc[1] += size[1]
        gallStr = f'{galleons} Galleons'
        sickleStr = f'{sickles} Sickels'
        knutStr = f'{knuts} Knuts'
        coinStrs = [gallStr, sickleStr, knutStr]
        for coin in coinStrs:
            size = font.size(coin)
            text = font.render(coin, True, BLACK, WHITE)
            self.menu_image.blit(text, (self.width-size[0],blitLoc[1]))
            blitLoc[1] += size[1]
        itemsLabel = "Items"
        text = font.render(itemsLabel, True, BLACK, WHITE)
        size = font.size(itemsLabel)
        self.menu_image.blit(text, (0,blitLoc[1]))
        blitLoc[1] += size[1]
        for item in self.items:
            cost = self.items[item]
            costStr = f'{cost[0]} g, {cost[1]} s, {cost[2]} k'
            costSize = font.size(costStr)
            costBlit = font.render(costStr, True, BLACK, WHITE)
            text = font.render(item, True, BLACK, WHITE)
            height = font.size(item)[1]
            self.menu_image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            self.menu_image.blit(costBlit, (self.width-costSize[0], blitLoc[1]))
            heightChange = max(height, costSize[1])
            Locs.append((blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += heightChange
        self.fontLocs = Locs

    def draw_selection_box(self):
        if self.selection == True:
            item_list = list(self.items.keys())
            item = item_list[self.selectionCount]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(item, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(item)[1]
            cost = self.items[item]
            costStr = f'{cost[0]} g, {cost[1]} s, {cost[2]} k'
            costSize = font.size(costStr)
            costBlit = font.render(costStr, True, WHITE, BLACK)
            height = max(height, costSize[1])
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
            self.menu_image.blit(selectionBox, (0,self.fontLocs[self.selectionCount][1]))
            self.menu_image.blit(text, (10,self.fontLocs[self.selectionCount][1]))
            self.menu_image.blit(costBlit, (self.width-costSize[0], self.fontLocs[self.selectionCount][1]))

    def wait_for_key_up(self):
        state = self.dialog_state
        self.dialog_state = 'waiting'
        hit_space = False
        while not hit_space:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    #next
                    if event.key == pg.K_SPACE:
                        hit_space = True
        self.dialog_state = state

    def buy(self):
        item_list = list(self.items.keys())
        item = item_list[self.selectionCount]
        self.purchased_item = item_list[self.selectionCount]
        #get item cost
        cost = self.items[item]
        cost_knuts = cost[0]*493 + cost[1]* 29 + cost[2]
        #get player money
        galleons = self.game.player.galleons
        sickles = self.game.player.sickles
        knuts = self.game.player.knuts
        player_knuts = galleons*493 + sickles*29 + knuts
        #check if they have enough
        if cost_knuts > player_knuts:
            self.text = "You don't have enough money for that!"
        else:
            if self.shop.shop.check_for_special_buy():
                self.shop.shop.special_buy(self, self.purchased_item)
            else:
                self.purchased_item = self.shop.shop.items[item]['Item']
            #pay and recieve item
            remaining_knuts = player_knuts - cost_knuts
            galleons = remaining_knuts // 493
            print(f'{galleons} galleons')
            remaining_knuts -= galleons*493
            sickles = remaining_knuts // 29
            print(f'{galleons} galleons')
            print(f'{sickles} sickles')
            remaining_knuts -= sickles*29
            knuts = remaining_knuts
            print(f'{galleons} galleons')
            print(f'{sickles} sickles')
            print(f'{knuts} knuts')
            self.game.player.inventory.append(self.purchased_item)
            #set player money
            self.game.player.galleons = galleons
            self.game.player.sickles = sickles
            self.game.player.knuts = knuts
            self.continue_shopping()

    def continue_shopping(self):
        self.text = 'Would you like to continue shopping?'
        self.dialog_state = 'question'

    def answer(self):
        if self.text == 'Would you like to continue shopping?' and self.ans == 'yes':
            self.text = f'Welcome to {self.shop.shop.name}!'
            self.dialog_state = 'dialog'
        if self.text == 'Would you like to continue shopping?' and self.ans == 'no':
            self.dialog_state = 'dialog'
            self.text = f'Enjoy your {self.purchased_item.name}!'
            self.draw()
            self.wait_for_key_up()
            self.close_shop()

    def close_shop(self):
        self.text = None
        self.selection = False
        self.shop = None
        self.selectionCount = 0
        self.purchased_item = None
        self.game.shop = None
        self.game.textbox.close_box()
        self.game.current_state = 'gameplay'

    def update(self):
        if self.shop != None:
            self.shop.update()
            self.get_shop_dialog()
        else:
            print('Getting Shop')
            self.get_shop()
            self.get_items()

class MenuState():
    def __init__(self, game):
        self.game = game
        self.menu_state = 'main'
        self.menu_dict = {
                'main' : SideMenuMainState(self, self.game),
                'Inventory' : InventoryState(self, self.game),
                'Spellbooks' : SpellbookState(self, self.game),
                'Quest Guide' : QuestGuideState(self, self.game),
                'Save' : SaveState(self, self.game)
        }

    def close_menu(self):
        self.menu_state = 'main'
        self.game.current_state = 'gameplay'
    #Draw Side Menu
    def draw(self):
        self.menu_dict[self.menu_state].draw()
    #Create dict of menus (inventory, spells, etc.)
    def open_inventory(self):
        self.menu_state = 'Inventory'
    #Main menu lists other menus
    #Selected Menu (new state) then displayed
    #Get Events
    def events(self):
        self.menu_dict[self.menu_state].events()
    def update(self):
        pass
