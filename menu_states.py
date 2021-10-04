import pygame as pg
from settings import *

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
                if event.key == pg.K_m:
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
                if event.key == pg.K_m:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()

class SpellbookState():
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
                if event.key == pg.K_m:
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
                if event.key == pg.K_m:
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
                if event.key == pg.K_m:
                    self.selection = False
                    self.selectionCount = 0
                    self.menu.close_menu()
