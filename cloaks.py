from items import *

class HogwartsCloak(Cloak):
    def __init__(self, house):
        self.name = 'Hogwarts Cloak'
        super().__init__()
        self.house = house

cloak = HogwartsCloak('G')

print(path.isdir(cloak.accent_image_folder))



#Wand Images
cloak_down_img = [path.join(img_folder, 'f1.png'), path.join(img_folder, 'f2.png'), path.join(img_folder, 'f3.png'), path.join(img_folder, 'f4.png')]
cloak_up_img = [path.join(img_folder, 'b1.png'), path.join(img_folder, 'b2.png'), path.join(img_folder, 'b3.png'), path.join(img_folder, 'b4.png')]
cloak_left_img = [path.join(img_folder, 'l1.png'), path.join(img_folder, 'l2.png'), path.join(img_folder, 'l3.png'), path.join(img_folder, 'l4.png')]
cloak_right_img = [path.join(img_folder, 'r1.png'), path.join(img_folder, 'r2.png'), path.join(img_folder, 'r3.png'), path.join(img_folder, 'r4.png')]
cloak_down = [pg.image.load(cloak_down_img[0]), pg.image.load(cloak_down_img[1]), pg.image.load(cloak_down_img[2]), pg.image.load(cloak_down_img[3])]
cloak_up = [pg.image.load(cloak_up_img[0]), pg.image.load(cloak_up_img[1]), pg.image.load(cloak_up_img[2]), pg.image.load(cloak_up_img[3])]
cloak_left = [pg.image.load(cloak_left_img[0]), pg.image.load(cloak_left_img[1]), pg.image.load(cloak_left_img[2]), pg.image.load(cloak_left_img[3])]
cloak_right = [pg.image.load(cloak_right_img[0]), pg.image.load(cloak_right_img[1]), pg.image.load(cloak_right_img[2]), pg.image.load(cloak_right_img[3])]
self.images = [cloak_down, cloak_up, cloak_left, cloak_right]
self.change_color()
