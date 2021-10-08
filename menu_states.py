import pygame as pg
from settings import *
from items import *

class SideMenuMainState():
    def __init__(self, menu, game):
        self.game = game
        self.menu = menu
        self.selection = False
        self.selectionCount = 0
        self.fontLocs = []

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount -= 1
                    self.selectionCount += 1
                    if self.selectionCount > len(self.menu.menu_dict.keys())-2:
                        self.selectionCount=0
                #scroll up
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount += 1
                    self.selectionCount -= 1
                    if self.selectionCount < 0:
                        self.selectionCount = len(self.menu.menu_dict.keys())-2
                if event.key == pg.K_SPACE:
                    self.select()
                if event.key == pg.K_m or event.key == pg.K_c:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()

    def draw(self):
        self.game.side_menu.clear()
        self.draw_text()
        self.draw_selection_box()
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.game.side_menu.image, (800,30))
        pg.display.flip()
    #Create dict of menus (inventory, spells, etc.)
    def draw_text(self):
        locs = []
        menus = list(self.menu.menu_dict.keys())
        blitLoc = [0,0]
        font = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        label = 'Main Menu'
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0]+25,blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        for menu in menus:
            if menu != 'main':
                text = font.render(menu, True, BLACK, WHITE)
                height = font.size(menu)[1]
                self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
                locs.append((blitLoc[0]+10,blitLoc[1]))
                blitLoc[1] += height
        self.fontLocs = locs

    def draw_selection_box(self):
        if self.selection == True:
            menu_list = [key for key in self.menu.menu_dict.keys() if key != 'main']
            menu = menu_list[self.selectionCount]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(menu, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(menu)[1]
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
            self.game.side_menu.image.blit(selectionBox, (0,self.fontLocs[self.selectionCount][1]))
            self.game.side_menu.image.blit(text, (10,self.fontLocs[self.selectionCount][1]))

    def select(self):
        menus = [key for key in self.menu.menu_dict.keys() if key != 'main']
        self.menu.menu_state = menus[self.selectionCount]
        self.selection = False

class InventoryState():
    def __init__(self, menu, game):
        self.game = game
        self.menu = menu
        self.inv_state = 'inventory'
        self.selection = False
        self.selectionCount = 0
        self.fontLocs = []
        self.width = 224
        #Action Box
        self.selected_item = None
        self.action_box = pg.Surface((0,0))
        self.act_box_sel_count = 0
        self.act_box_font_locs = []

    def draw(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        self.game.draw_grid()
        for sprite in self.game.all_sprites:
            sprite.draw(self.game)
        self.game.side_menu.clear()
        self.draw_text()
        self.draw_selection_box()
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.game.side_menu.image, (800,30))
        if self.inv_state == 'action_box':
            self.game.screen.blit(self.action_box, (650,self.fontLocs[self.selectionCount][1]+30))
            self.draw_act_box_text()
            self.draw_act_box_sel_box()
        pg.display.flip()

    def draw_text(self):
        locs = []
        blitLoc = [0,0]
        font = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        label = self.menu.menu_state
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0]+25,blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        #Get Player Money
        galleons = self.game.player.galleons
        sickles = self.game.player.sickles
        knuts = self.game.player.knuts
        #Draw Money Text
        moneyLabel = "Money"
        text = font.render(moneyLabel, True, BLACK, WHITE)
        size = font.size(moneyLabel)
        centerX = size[0]//2
        self.game.side_menu.image.blit(text, (0,blitLoc[1]))
        blitLoc[1] += size[1]
        gallStr = f'{galleons} Galleons'
        sickleStr = f'{sickles} Sickels'
        knutStr = f'{knuts} Knuts'
        coinStrs = [gallStr, sickleStr, knutStr]
        for coin in coinStrs:
            size = font.size(coin)
            text = font.render(coin, True, BLACK, WHITE)
            self.game.side_menu.image.blit(text, (self.width-size[0],blitLoc[1]))
            blitLoc[1] += size[1]
        #Draw Item Text
        itemsLabel = "Equipped"
        text = font.render(itemsLabel, True, BLACK, WHITE)
        size = font.size(itemsLabel)
        self.game.side_menu.image.blit(text, (0,blitLoc[1]))
        blitLoc[1] += size[1]
        for item in self.game.player.equipped:
            text = font.render(item.name, True, BLACK, WHITE)
            height = font.size(item.name)[1]
            self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            locs.append((blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += height
        if len(self.game.player.equipped) == 0:
            text = font.render('No equipped items', True, BLACK, WHITE)
            height = font.size('No equipped items')[1]
            self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += height
        itemsLabel = "Items"
        text = font.render(itemsLabel, True, BLACK, WHITE)
        size = font.size(itemsLabel)
        self.game.side_menu.image.blit(text, (0,blitLoc[1]))
        blitLoc[1] += size[1]
        for item in self.game.player.inventory:
            text = font.render(item.name, True, BLACK, WHITE)
            height = font.size(item.name)[1]
            self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            locs.append((blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += height
        self.fontLocs = locs

    def draw_selection_box(self):
        if self.selection == True:
            items = [item.name for item in self.game.player.equipped]
            items += [item.name for item in self.game.player.inventory]
            item = items[self.selectionCount]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(item, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(item)[1]
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
            self.game.side_menu.image.blit(selectionBox, (0,self.fontLocs[self.selectionCount][1]))
            self.game.side_menu.image.blit(text, (10,self.fontLocs[self.selectionCount][1]))

    def open_actions_box(self, item):
        self.act_box_font_locs = []
        self.action_box = pg.Surface((150,300))
        self.action_box.fill(WHITE)
        font = pg.font.Font('freesansbold.ttf', 12)
        blitLoc = [0,0]
        for action in item.actions:
            size = font.size(action)
            text = font.render(action, True, BLACK, WHITE)
            self.action_box.blit(text, (0,blitLoc[1]))
            self.act_box_font_locs.append((blitLoc[0],blitLoc[1]))
            blitLoc[1] += size[1]

    def draw_act_box_text(self):
        self.act_box_font_locs = []
        self.action_box.fill(WHITE)
        font = pg.font.Font('freesansbold.ttf', 12)
        blitLoc = [0,0]
        for action in self.selected_item.actions:
            size = font.size(action)
            text = font.render(action, True, BLACK, WHITE)
            self.action_box.blit(text, (0,blitLoc[1]))
            self.act_box_font_locs.append((blitLoc[0],blitLoc[1]))
            blitLoc[1] += size[1]

    def draw_act_box_sel_box(self):
        if self.inv_state == 'action_box':
            actions = self.selected_item.actions
            action = actions[self.act_box_sel_count]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(action, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(action)[1]
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
        self.action_box.blit(selectionBox, (self.act_box_font_locs[self.act_box_sel_count]))
        self.action_box.blit(text, (self.act_box_font_locs[self.act_box_sel_count]))
        self.selected_action = action

    def equip(self, item):
        if isinstance(item, Equippable):
            self.game.player.equipped.append(item)
            self.game.player.inventory.remove(item)
            item.equip_effect(self.game)
            #Change alpha if invisible
            if isinstance(item, Wearable) and self.game.player.invisible:
                for img_list in item.images:
                    for img in img_list:
                        img.set_alpha(100)

        else:
            self.game.textbox.draw_box()
            text = f'{item.name} is not equippable!'
            self.game.textbox.draw_text(text)
            self.draw()
            self.wait_for_key_up()
            self.game.textbox.close_box()

    def unequip(self, item):
        self.game.player.equipped.remove(item)
        self.game.player.inventory.append(item)
        item.unequip_effect(self.game)
        #reset alpha if changed
        if isinstance(item, Wearable) and self.game.player.invisible:
            for img_list in item.images:
                for img in img_list:
                    img.set_alpha(255)

    def events(self):
        if self.inv_state == 'inventory':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.quit()
                if event.type == pg.KEYUP:
                    #Select Item
                    if event.key == pg.K_SPACE:
                        if not self.selection:
                            self.selection = True
                        else:
                            if len(self.game.player.equipped) != 0 and self.selectionCount < len(self.game.player.equipped):
                                self.selected_item = self.game.player.equipped[self.selectionCount]
                                self.open_actions_box(self.selected_item)
                                self.inv_state = 'action_box'
                            elif len(self.game.player.inventory) != 0 and self.selectionCount >= len(self.game.player.equipped):
                                self.selected_item = self.game.player.inventory[self.selectionCount - len(self.game.player.equipped)]
                                self.open_actions_box(self.selected_item)
                                self.inv_state = 'action_box'
                    #Scroll Down
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if not self.selection:
                            self.selection = True
                            self.selectionCount -= 1
                        self.selectionCount += 1
                        if self.selectionCount > len(self.game.player.inventory)+len(self.game.player.equipped)-1:
                            self.selectionCount=0
                    #scroll up
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if not self.selection:
                            self.selection = True
                            self.selectionCount += 1
                        self.selectionCount -= 1
                        if self.selectionCount < 0:
                            self.selectionCount = len(self.game.player.inventory)+len(self.game.player.equipped)-1
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.selection = False
                        self.selectionCount = 0
                        self.menu.menu_state = 'main'
                    #Equip Item
                    if event.key == pg.K_e:
                        if self.selection:
                            if len(self.game.player.equipped) != 0 and self.selectionCount < len(self.game.player.equipped):
                                self.unequip(self.game.player.equipped[self.selectionCount])
                            elif len(self.game.player.inventory) != 0 and self.selectionCount >= len(self.game.player.equipped):
                                self.equip(self.game.player.inventory[self.selectionCount - len(self.game.player.equipped)])
                    if event.key == pg.K_m or event.key == pg.K_c or event.key == pg.K_i:
                        self.selection = False
                        self.selectionCount = 0
                        self.menu.close_menu()

        elif self.inv_state == 'action_box':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        #select action here
                        #self.selected_item.action_dict[self.selected_action]
                        self.game.ItemHandler.do_action(self.selected_item, self.selected_action)
                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.action_box = pg.Surface((0,0))
                        self.act_box_sel_count = 0
                        self.act_box_font_locs = []
                        self.inv_state = 'inventory'
                    #Scroll Down
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.act_box_sel_count += 1
                        if self.act_box_sel_count > len(self.selected_item.actions)-1:
                            self.act_box_sel_count=0
                    #Scroll up
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        self.act_box_sel_count -= 1
                        if self.act_box_sel_count < 0:
                            self.act_box_sel_count = len(self.selected_item.actions)-1



    def wait_for_key_up(self):
        state = self.inv_state
        self.inv_state = 'waiting'
        hit_space = False
        while not hit_space:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    #next
                    if event.key == pg.K_SPACE:
                        hit_space = True
        self.inv_state = state

class SpellsState():
    def __init__(self, menu, game):
        self.game = game
        self.menu = menu
        self.selection = False
        self.selectionCount = 0
        self.fontLocs = []

    def draw(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        self.game.draw_grid()
        for sprite in self.game.all_sprites:
            sprite.draw(self.game)
        self.game.side_menu.clear()
        self.draw_text()
        self.draw_selection_box()
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.game.side_menu.image, (800,30))
        pg.display.flip()

    def draw_text(self):
        locs = []
        blitLoc = [0,0]
        font = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        label = self.menu.menu_state
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0]+25,blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        for spell in self.game.SpellHandler.known_spells:
            text = font.render(spell.name, True, BLACK, WHITE)
            height = font.size(spell.name)[1]
            self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            locs.append((blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += height
        self.fontLocs = locs

    def draw_selection_box(self):
        if self.selection == True:
            spells = [spell for spell in self.game.SpellHandler.known_spells]
            spell_names = [spell.name for spell in spells]
            spell = spell_names[self.selectionCount]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(spell, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(spell)[1]
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
            self.game.side_menu.image.blit(selectionBox, (0,self.fontLocs[self.selectionCount][1]))
            self.game.side_menu.image.blit(text, (10,self.fontLocs[self.selectionCount][1]))
            self.selected_spell = spells[self.selectionCount]

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount -= 1
                    self.selectionCount += 1
                    if self.selectionCount > len(self.game.SpellHandler.known_spells)-1:
                        self.selectionCount=0
                #scroll up
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount += 1
                    self.selectionCount -= 1
                    if self.selectionCount < 0:
                        self.selectionCount = len(self.game.SpellHandler.known_spells)-1

                if event.key == pg.K_SPACE:
                    self.game.SpellHandler.cast(self.selected_spell)

                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.menu_state = 'main'
                if event.key == pg.K_m or event.key == pg.K_c:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()

class QuestGuideState():
    def __init__(self, menu, game):
        self.game = game
        self.menu = menu
        self.selection = False
        self.selectionCount = 0
        self.fontLocs = []

    def draw(self):
        self.game.side_menu.clear()
        self.draw_text()
        self.draw_selection_box()
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.game.side_menu.image, (800,30))
        pg.display.flip()

    def draw_text(self):
        locs = []
        blitLoc = [0,0]
        font = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        label = self.menu.menu_state
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0]+25,blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        label = 'Main Quest'
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0],blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        for quest in self.game.main_quests:
            if quest.active:
                text = font.render(quest.name, True, BLACK, WHITE)
                height = font.size(quest.name)[1]
                self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
                locs.append((blitLoc[0]+10,blitLoc[1]))
                blitLoc[1] += height
        if len(self.game.main_quests) == 0:
            label = 'Add main quests later'
        text = font.render(label, True, BLACK, WHITE)
        size = font.size(label)
        self.game.side_menu.image.blit(text, (10,blitLoc[1]))
        blitLoc[1] += size[1]
        label = 'Active Side Quests'
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0],blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)
        for quest in self.game.quests:
            if quest.active:
                text = font.render(quest.name, True, BLACK, WHITE)
                height = font.size(quest.name)[1]
                self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
                locs.append((blitLoc[0]+10,blitLoc[1]))
                blitLoc[1] += height
        if len([quest for quest in self.game.quests if quest.active]) == 0:
            label = 'No Active Side Quests'
            text = font.render(label, True, BLACK, WHITE)
            height = font.size(label)[1]
            self.game.side_menu.image.blit(text, (blitLoc[0]+10,blitLoc[1]))
            blitLoc[1] += height

        self.fontLocs = locs

    def draw_selection_box(self):
        if self.selection == True:
            quests = [quest.name for quest in self.game.main_quests if quest.active]
            quests += [quest.name for quest in self.game.quests if quest.active]
            quest = quests[self.selectionCount]
            #Get font and font data
            font = pg.font.Font('freesansbold.ttf', 12)
            text = font.render(quest, True, WHITE, BLACK)
            textRect = text.get_rect()
            height = font.size(quest)[1]
            selectionBox = pg.Surface((300,height))
            #Draw Selection Box then text
            self.game.side_menu.image.blit(selectionBox, (0,self.fontLocs[self.selectionCount][1]))
            self.game.side_menu.image.blit(text, (10,self.fontLocs[self.selectionCount][1]))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount -= 1
                    self.selectionCount += 1
                    if self.selectionCount > len([quest for quest in self.game.main_quests if quest.active]) + len([quest for quest in self.game.quests if quest.active])-1:
                        self.selectionCount=0
                #scroll up
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount += 1
                    self.selectionCount -= 1
                    if self.selectionCount < 0:
                        self.selectionCount = len([quest for quest in self.game.main_quests if quest.active]) + len([quest for quest in self.game.quests if quest.active])-1
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.menu_state = 'main'
                if event.key == pg.K_m or event.key == pg.K_c:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()

class SaveState():
    def __init__(self, menu, game):
        self.game = game
        self.menu = menu
        self.selection = False
        self.selectionCount = 0
        self.fontLocs = []

    def draw(self):
        self.game.side_menu.clear()
        self.draw_text()
        #self.draw_selection_box()
        self.game.screen.blit(self.game.textbox.image, (20,500))
        self.game.screen.blit(self.game.side_menu.image, (800,30))
        pg.display.flip()

    def draw_text(self):
        locs = []
        blitLoc = [0,0]
        font = pg.font.Font(f'{font_folder}/MagicFont.ttf', 36)
        label = self.menu.menu_state
        text = font.render(label, True, BLACK, WHITE)
        height = font.size(label)[1]
        self.game.side_menu.image.blit(text, (blitLoc[0]+25,blitLoc[1]))
        blitLoc[1] += height
        font = pg.font.Font('freesansbold.ttf', 12)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount -= 1
                    self.selectionCount += 1
                    if self.selectionCount > len(self.menu.menu_dict.keys())-2:
                        self.selectionCount=0
                #scroll up
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if not self.selection:
                        self.selection = True
                        self.selectionCount += 1
                    self.selectionCount -= 1
                    if self.selectionCount < 0:
                        self.selectionCount = len(self.menu.menu_dict.keys())-2
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.menu_state = 'main'
                if event.key == pg.K_m or event.key == pg.K_c:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()
