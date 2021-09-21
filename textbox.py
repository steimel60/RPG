import pygame as pg

class Textbox():
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((300, 100))
        self.image.fill(BLACK)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
