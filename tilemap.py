import pygame as pg
import pytmx
from os import path
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0]) #number of tiles wide
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE #pixel size
        self.height = self.tileheight * TILESIZE #pixel size


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, door_id, to_level, exit_dir):
        self.groups = game.all_sprites, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y
        self.door_id = door_id
        self.to_level = to_level
        self.exit_dir = exit_dir

    def draw(self, game):
        pass


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height =tm.height * tm.tileheight
        self.tmxdata = tm

    def render (self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render (temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move (self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(screenWidth / 2)
        y = -target.rect.y + int(screenHeight / 2)

        ## limit scrolling to map size
        x = min(0,x) # left
        x = max(-(self.width - screenWidth), x) # right
        y = min(0,y) # top
        y = max(-(self.height - screenHeight), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
