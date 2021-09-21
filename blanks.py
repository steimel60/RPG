from settings import *
from os import path
import pygame as pg

#### Body Images ####
walk_down_img = [path.join(img_folder, 'f1.png'), path.join(img_folder, 'f2.png'), path.join(img_folder, 'f3.png'), path.join(img_folder, 'f4.png')]
walk_up_img = [path.join(img_folder, 'b1.png'), path.join(img_folder, 'b2.png'), path.join(img_folder, 'b3.png'), path.join(img_folder, 'b4.png')]
walk_left_img = [path.join(img_folder, 'l1.png'), path.join(img_folder, 'l2.png'), path.join(img_folder, 'l3.png'), path.join(img_folder, 'l4.png')]
walk_right_img = [path.join(img_folder, 'r1.png'), path.join(img_folder, 'r2.png'), path.join(img_folder, 'r3.png'), path.join(img_folder, 'r4.png')]

body_images = [walk_down_img[:], walk_up_img[:], walk_left_img[:], walk_right_img[:]]
user_skin_color = (255, 255, 255)

#### Hair images ####
messy_hair = [path.join(img_folder, 'h1f.png'), path.join(img_folder, 'h1b.png'), path.join(img_folder, 'h1l.png'), path.join(img_folder, 'h1r.png')]
clean_hair = [path.join(img_folder, 'h2f.png'), path.join(img_folder, 'h2b.png'), path.join(img_folder, 'h2l.png'), path.join(img_folder, 'h2r.png')]
long_hair = [path.join(img_folder, 'h3f.png'), path.join(img_folder, 'h3b.png'), path.join(img_folder, 'h3l.png'), path.join(img_folder, 'h3r.png')]
afro_hair = [path.join(img_folder, 'h4f.png'), path.join(img_folder, 'h4b.png'), path.join(img_folder, 'h4l.png'), path.join(img_folder, 'h4r.png')]

hair_list = [messy_hair, clean_hair, long_hair, afro_hair]
hairColors = [BLACK, YELLOW, RED, GREEN]

### Skin Select
def skin_select(game):
    menuCount = 0
    game = game
    global user_skin_color
    original_color = user_skin_color
    color_selection = True
    while color_selection:
        pg.time.delay(150)
        pg.event.get()
        keys = pg.key.get_pressed()
        skin_colors = [(245,185,158),(234,154,95),(127,67,41)]

        if keys[pg.K_RIGHT]:
            menuCount += 1
            new_color = skin_colors[menuCount % 3]
            change_color(game.player_img, user_skin_color, new_color)
            user_skin_color = new_color
            game.draw()

        if keys[pg.K_LEFT]:
            menuCount -= 1
            new_color = skin_colors[menuCount % 3]
            change_color(game.player_img, user_skin_color, new_color)
            user_skin_color = new_color
            game.draw()

        if keys[pg.K_RETURN]:
            color_selection = False
        if keys[pg.K_ESCAPE]:
            change_color(game.player_img, user_skin_color, original_color)
            color_selection = False

###Color Change Func
def change_color(img_list, old_color, new_color):
    flat_list = flatten(img_list)
    for img in flat_list:
        img_arr = pg.PixelArray(img)
        img_arr.replace (old_color, new_color)
        del img_arr

## Flatten image lists
def flatten(L):
    if len(L) == 1:
        if isinstance(L[0], list):
            result = flatten(L[0])
        else:
            result = L
    elif isinstance(L[0], list):
        result = flatten(L[0]) +flatten(L[1:])
    else:
        result = [L[0]] + flatten(L[1:])
    return result
