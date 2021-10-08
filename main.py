import pygame as pg
import sys, states
from os import path
from settings import *
from Quests import *
from sprites import *
from tilemap import *
from shops import *
import random

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screenWidth, screenHeight))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250,100)
        self.load_data('test')
        self.player = None
        self.main_quests = self.init_main_quests()
        self.quests = self.init_quests()
        self.menus = []
        self.shop = None
        self.STATE_DICT = {
            'gameplay': states.GameplayState(self),
            'shop' : states.ShopState(self),
            'menu' : states.MenuState(self)
        }
        self.current_state = 'gameplay'

    def init_quests(self):
        quest1 = TestQuest(self)
        quest2 = TradeWithLoren(self)
        quests = [quest1, quest2]
        return quests

    def init_main_quests(self):
        quests = []

        return quests

    def load_data(self, level):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'Maps')
        self.level = level
        self.map = TiledMap(path.join(map_folder, self.level + '.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self, from_door=[False]):
        self.all_sprites = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.user_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.walk_paths = pg.sprite.Group()
        self.gates = pg.sprite.Group()
        self.shops = []
        #Load Data from Tiled Map
        for tile_object in self.map.tmxdata.objects:
            if not from_door[0]:
                if tile_object.name == "player":
                    self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall" or tile_object.name == "shop":
                self.wall = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "door":
                self.door = Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.door_id, tile_object.to_level, tile_object.exit_dir)
            if tile_object.name == "NPC":
                self.npc = NPC(self, tile_object.dir, tile_object.x, tile_object.y, tile_object.path_id, tile_object.name_id, tile_object.skin_id, tile_object.hair_id, tile_object.hair_color)
            if tile_object.name == "walk_path":
                self.walk_path = Walk_Path(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.path_id)
            if tile_object.name == "shop":
                self.loaded_shop = Shop(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.shop_id)
                self.shops.append(self.loaded_shop)
            if tile_object.name == "gate":
                self.loaded_shop = Gate(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.level, tile_object.locked)
        #Load Level by Door Data
        if from_door[0]:
            #Check if player went through door
            for door in self.doors:
                if door.door_id == from_door[1]:
                    #Place player by door they came out of
                    if from_door[2] == 'up':
                        self.player = Player(self, door.x, door.y-TILESIZE, inventory=self.player.inventory, money=(self.player.galleons,self.player.sickles,self.player.knuts))
                        self.player.dir = 1
                        self.player.equipped_effects()
                    elif from_door[2] == 'down':
                        self.player = Player(self, door.x, door.y+TILESIZE, inventory=self.player.inventory, money=(self.player.galleons,self.player.sickles,self.player.knuts))
                        self.player.dir = 0
                        self.player.equipped_effects()
                    elif from_door[2] == 'left':
                        self.player = Player(self, door.x-TILESIZE, door.y, inventory=self.player.inventory, money=(self.player.galleons,self.player.sickles,self.player.knuts))
                        self.player.dir = 2
                        self.player.equipped_effects()
                    elif from_door[2] == 'right':
                        self.player = Player(self, door.x+TILESIZE, door.y, inventory=self.player.inventory, money=(self.player.galleons,self.player.sickles,self.player.knuts))
                        self.player.dir = 3
                        self.player.equipped_effects()
        #Set Others
        self.camera = Camera(self.map.width, self.map.height)
        self.textbox = Textbox(self, self.player.x, self.player.y)
        self.side_menu = SideMenu(self)

    def check_level(self):
        for door in self.doors:
            for player in self.user_group:
                if (player.x >= door.x and player.x<door.x+door.w) and (player.y == door.y):
                    self.level = door.to_level
                    door_id = door.door_id
                    exit_dir = door.exit_dir
                    self.load_data(self.level)
                    self.new(from_door=[True,door_id,exit_dir])

###Game Loop
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    #Update
    def update(self):
        self.STATE_DICT[self.current_state].update()

    def draw_grid(self):
        for x in range(0, screenWidth, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x,0), (x, screenHeight))
        for y in range(0, screenHeight, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (screenWidth, y))

    def draw(self):
        self.STATE_DICT[self.current_state].draw()

    def events(self):
        self.STATE_DICT[self.current_state].events()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
