import pygame as pg
import sys
from os import path
from settings import *
from Quests import *
from sprites import *
from tilemap import *
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
        self.quests = self.init_quests()
        self.menus = []

    def init_quests(self):
        quest1 = TestQuest(self)
        quest2 = TradeWithLoren(self)
        quests = [quest1, quest2]

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

        for tile_object in self.map.tmxdata.objects:
            if not from_door[0]:
                if tile_object.name == "player":
                    self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                self.wall = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "door":
                self.wall = Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.door_id, tile_object.to_level, tile_object.exit_dir)
            if tile_object.name == "NPC":
                self.npc = NPC(self, tile_object.x, tile_object.y, tile_object.path_id, tile_object.name_id, tile_object.skin_id, tile_object.hair_id, tile_object.hair_color)
            if tile_object.name == "walk_path":
                self.walk_path = Walk_Path(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.path_id)

        if from_door[0]:
            #Check if player went through door
            for door in self.doors:
                if door.door_id == from_door[1]:
                    #Place player by door they came out of
                    if from_door[2] == 'up':
                        self.player = Player(self, door.x, door.y-TILESIZE, inventory=self.player.inventory)
                        self.player.dir = 1
                    elif from_door[2] == 'down':
                        self.player = Player(self, door.x, door.y+TILESIZE, inventory=self.player.inventory)
                        self.player.dir = 0
                    elif from_door[2] == 'left':
                        self.player = Player(self, door.x-TILESIZE, door.y, inventory=self.player.inventory)
                        self.player.dir = 2
                    elif from_door[2] == 'right':
                        self.player = Player(self, door.x+TILESIZE, door.y, inventory=self.player.inventory)
                        self.player.dir = 3

        self.camera = Camera(self.map.width, self.map.height)
        self.textbox = Textbox(self, self.player.x, self.player.y)
        self.inventory = InventoryBox(self, self.player.x, self.player.y)
        self.menus = [self.inventory]

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
        for menu in self.menus:
            if not menu.open:
                self.all_sprites.update()
                self.textbox.update()
                self.camera.update(self.player)
                self.check_level()

    def draw_grid(self):
        for x in range(0, screenWidth, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x,0), (x, screenHeight))
        for y in range(0, screenHeight, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (screenWidth, y))

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.textbox.image, (20,500))
        self.screen.blit(self.inventory.image, (800,30))
        pg.display.flip()

    def events(self):
        menu_open = False
        for menu in self.menus:
            if menu.open:
                menu.events()
                menu_open = True
        # catch all events here
        if not menu_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        self.player.check_for_interactions()
                    if event.key == pg.K_i:
                        self.inventory.switch()
                keys = pg.key.get_pressed()
                #if keys[pg.K_c]:
                    #skin_select(self)

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
