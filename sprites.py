import pygame as pg
from settings import *
from items import *
from dialouges import *
from specialNPCs import *
from houses import GryffindorHouse, SlytherinHouse, HufflepuffHouse, RavenclawHouse
from blanks import change_color, img_folder, game_folder, walk_up_img, walk_down_img, walk_left_img, walk_right_img, hair_list, hairColors
from os import path
import random
from NPC_data import Special_NPCs, RandomNPCDataGenerator

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.user_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        user_down = [pg.image.load(walk_down_img[0]), pg.image.load(walk_down_img[1]), pg.image.load(walk_down_img[2]), pg.image.load(walk_down_img[3])]
        user_up = [pg.image.load(walk_up_img[0]), pg.image.load(walk_up_img[1]), pg.image.load(walk_up_img[2]), pg.image.load(walk_up_img[3])]
        user_left = [pg.image.load(walk_left_img[0]), pg.image.load(walk_left_img[1]), pg.image.load(walk_left_img[2]), pg.image.load(walk_left_img[3])]
        user_right = [pg.image.load(walk_right_img[0]), pg.image.load(walk_right_img[1]), pg.image.load(walk_right_img[2]), pg.image.load(walk_right_img[3])]
        self.images = [user_down, user_up, user_left, user_right]
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.hair_down = pg.image.load(hair_list[0][0])
        self.hair_up = pg.image.load(hair_list[0][1])
        self.hair_left = pg.image.load(hair_list[0][2])
        self.hair_right = pg.image.load(hair_list[0][3])
        self.hair = [self.hair_down, self.hair_up, self.hair_left, self.hair_right]
        self.rect = self.image.get_rect()
        self.dir = 0
        self.x = x
        self.y = y
        self.invisible = False
        #Wearables
        self.hat = None
        self.cloak = None
        self.shirt = None
        self.pants = None
        self.wand = None
        #Movement
        self.speed = WALK_SPEED
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.hit_box_x = x + TILESIZE
        self.hit_box_y = y + TILESIZE
        self.walk_count = 0
        self.initial_collide = False
        self.dir = 0

    def move(self):
        if self.walk_count + 1 > 23:
            self.walk_count = 0
        #if self.moving:
        if self.target_x > self.x: #rightt
            self.x += self.speed
            self.walk_count += 1
            self.dir = 3
        elif self.target_x < self.x: #left
            self.x -= self.speed
            self.walk_count += 1
            self.dir = 2
        elif self.target_y > self.y: #down
            self.y += self.speed
            self.walk_count += 1
            self.dir = 0
        elif self.target_y < self.y: #up
            self.y -= self.speed
            self.walk_count += 1
            self.dir = 1
        else:
            self.target_x = self.x
            self.target_y = self.y
            self.walk_count = 0
            self.image = self.images[self.dir][self.walk_count]
        if self.target_x == self.x and self.target_y == self.y:
            self.moving = False

    def get_keys(self):
        keys = pg.key.get_pressed()
        old_x = self.x
        old_y = self.y
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.moving == False:
            self.target_x -= TILESIZE
            self.dir = 2
            self.moving = True
        elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.moving == False:
            self.target_x += TILESIZE
            self.dir = 3
            self.moving = True
        elif (keys[pg.K_UP] or keys[pg.K_w]) and self.moving == False:
            self.target_y -= TILESIZE
            self.dir = 1
            self.moving = True
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and self.moving == False:
            self.target_y += TILESIZE
            self.dir = 0
            self.moving = True
        if self.collides():
            self.target_x = old_x
            self.target_y = old_y

    def collide_with_walls(self):
        for wall in self.game.walls:
            if wall.x <= self.target_x < (wall.x + wall.w) and wall.y <= self.target_y + TILESIZE < (wall.y + wall.h):
                return True
        return False

    def collide_with_npc(self):
        for npc in self.game.npcs:
            if abs(self.target_x - npc.x) < TILESIZE and abs(self.target_y - npc.y) < TILESIZE:
                self.initial_collide = True
                return True
        return False

    def collide_with_gates(self):
        for gate in self.game.gates:
            if gate.locked:
                if gate.x <= self.target_x < (gate.x + gate.w) and gate.y <= self.target_y + TILESIZE < (gate.y + gate.h):
                    return True
        return False

    def collides(self):
        if self.collide_with_npc() or self.collide_with_walls() or self.collide_with_gates():
            return True
        return False

    def get_image(self):
        self.images[self.dir][self.walk_count // 6].blit(self.hair[self.dir], (0,0))
        self.image = self.images[self.dir][self.walk_count // 6]

    def draw(self, game):
        game.screen.blit(self.image, self.game.camera.apply(self))
        for item in [self.hat, self.pants, self.shirt, self.cloak, self.wand]:
            if item != None:
                game.screen.blit(item.images[self.dir][self.walk_count // 6], self.game.camera.apply(self))

    def check_for_interactions(self):
        if self.dir == 0: #down
            for interactable in self.game.interactables:
                if interactable.x == self.x and interactable.y == self.y + TILESIZE:
                    interactable.dir=1
                    interactable.check_interactions()
        if self.dir == 1: #up
            for interactable in self.game.interactables:
                if interactable.x == self.x and interactable.y + interactable.h - TILESIZE == self.y:
                    interactable.dir=0
                    interactable.check_interactions()
        if self.dir == 2: #left
            for interactable in self.game.interactables:
                if interactable.x == self.x - TILESIZE and interactable.y == self.y:
                    interactable.dir=3
                    interactable.check_interactions()
        if self.dir == 3: #right
            for interactable in self.game.interactables:
                if interactable.x == self.x + TILESIZE and interactable.y == self.y:
                    interactable.dir=2
                    interactable.check_interactions()

    def equipped_effects(self):
        for item in self.game.ItemHandler.equipped:
            item.equip_effect(self.game)

    def update(self):
        self.get_keys()
        self.collides()
        self.get_image()
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y
        self.get_image()

class NPC(pg.sprite.Sprite):
    def __init__(self, game, dir, x, y, name_id):
        ### Get or Randomize Features ###
        self.generator = self.check_if_special_npc(name_id)
        self.name_id = name_id
        self.name = self.get_npc_attribute('Name')
        skin_id = self.get_npc_attribute('Skin ID')
        hair_id = self.get_npc_attribute('Hair ID')
        hair_color = self.get_npc_attribute('Hair Color')
        self.hat = None
        self.cloak = self.get_npc_attribute('Cloak')
        self.shirt = self.get_npc_attribute('Shirt')
        self.pants = self.get_npc_attribute('Pants')
        self.wand = None
        ### Load Images ###
        npc_down = [pg.image.load(walk_down_img[0]), pg.image.load(walk_down_img[1]), pg.image.load(walk_down_img[2]), pg.image.load(walk_down_img[3])]
        npc_up = [pg.image.load(walk_up_img[0]), pg.image.load(walk_up_img[1]), pg.image.load(walk_up_img[2]), pg.image.load(walk_up_img[3])]
        npc_left = [pg.image.load(walk_left_img[0]), pg.image.load(walk_left_img[1]), pg.image.load(walk_left_img[2]), pg.image.load(walk_left_img[3])]
        npc_right = [pg.image.load(walk_right_img[0]), pg.image.load(walk_right_img[1]), pg.image.load(walk_right_img[2]), pg.image.load(walk_right_img[3])]
        self.images = [npc_down, npc_up, npc_left, npc_right]
        change_color(self.images, WHITE, skin_colors[skin_id])
        self.hair = [pg.image.load(hair_list[hair_id][0]), pg.image.load(hair_list[hair_id][1]), pg.image.load(hair_list[hair_id][2]), pg.image.load(hair_list[hair_id][3])]
        change_color(self.hair, WHITE, hairColors[hair_color])
        ### Add to game groups ###
        self.groups = game.all_sprites, game.npcs, game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        ### Surface and Collision Rect ###
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.images[0][0]
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.h = TILESIZE*2
        self.w = TILESIZE
        ### Movement Control ###
        self.moving = False
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.walk_count = 0
        self.dir = dir
        self.initial_collide = False
        self.collide_wait = False
        self.text = False
        #Testing
        self.on_path = False
        self.path_min_x = None
        self.path_max_x = None
        self.path_min_y = None
        self.path_max_y = None
        ### Unique IDs ###
        self.introduced = False
        self.wander_wait = 1000

    def move(self):
        if self.walk_count + 1 > 23 or not self.moving:
            self.walk_count = 0
        if self.moving and not self.initial_collide:
            """
            move by 4 pixles until reaching target x,y
            """
            self.initial_collide = False
            self.collide_wait = True  ## Player has moved since first colliding
            if self.target_x > self.x: #right
                self.x += WALK_SPEED
                self.walk_count += 1
                self.dir = 3
            elif self.target_x < self.x: #left
                self.x -= WALK_SPEED
                self.walk_count += 1
                self.dir = 2
            elif self.target_y > self.y: #down
                self.y += WALK_SPEED
                self.walk_count += 1
                self.dir = 0
            elif self.target_y < self.y: #up
                self.y -= WALK_SPEED
                self.walk_count += 1
                self.dir = 1
            else:
                self.moving = False

    def wander(self):
        if not self.moving and not self.initial_collide:
            self.wander_wait += self.game.dt
            randome_wait_time = random.choice([1,2,2.3,2.5,3,3.1])
            if self.wander_wait > randome_wait_time:
                #Get possible distances by dir
                left_tile_range = int((self.x - self.path_min_x)//TILESIZE)
                right_tile_range = int((self.path_max_x - self.x)//TILESIZE)
                up_tile_range = int((self.y - self.path_min_y)//TILESIZE)
                down_tile_range = int((self.path_max_y - self.y)//TILESIZE)
                #Pick random direction
                possible_dirs = []
                if left_tile_range != 0:
                    possible_dirs.append('left')
                if right_tile_range != 0:
                    possible_dirs.append('right')
                if up_tile_range != 0:
                    possible_dirs.append('up')
                if down_tile_range != 0:
                    possible_dirs.append('down')
                dir = random.choice(possible_dirs)
                #Set Target Loc
                if dir =='left' and left_tile_range != 0:
                    tile_count = random.choice([x for x in range(left_tile_range)])
                    if tile_count != 0:
                        self.target_x -= tile_count*TILESIZE
                        self.dir = 2
                        self.moving = True
                if dir =='right' and right_tile_range != 0:
                    tile_count = random.choice([x for x in range(right_tile_range)])
                    if tile_count != 0:
                        self.target_x += tile_count*TILESIZE
                        self.dir = 3
                        self.moving = True
                if dir =='up' and up_tile_range != 0:
                    tile_count = random.choice([x for x in range(up_tile_range)])
                    if tile_count != 0:
                        self.target_y -= tile_count*TILESIZE
                        self.dir = 1
                        self.moving = True
                if dir =='down' and down_tile_range != 0:
                    tile_count = random.choice([x for x in range(down_tile_range)])
                    if tile_count != 0:
                        self.target_y += tile_count*TILESIZE
                        self.dir = 0
                        self.moving = True
                self.wander_wait = 0

    def find_path(self):
        for path in self.game.walk_paths:
            if self.x >= path.x and self.x + self.w <= path.x + path.w and self.y >= path.y and self.y + TILESIZE <= path.y + path.h:
                self.on_path = True
                self.path_min_x = path.x
                self.path_max_x = path.x + path.w - self.w
                self.path_min_y = path.y
                self.path_max_y = path.y + path.h - TILESIZE
                self.wander()

    def collides(self):
        if self.moving and not self.initial_collide:
            for player in self.game.user_group:
                if player.target_x == self.x and player.target_y == self.y + TILESIZE and self.dir == 0:
                    self.moving = False
                    self.walk_count = 0
                    player.dir = 1
                    self.initial_collide = True
                if player.target_x == self.x and player.target_y == self.y - TILESIZE and self.dir == 1:
                    self.moving = False
                    self.walk_count = 0
                    player.dir = 0
                    self.initial_collide = True
                if player.target_x == self.x - TILESIZE and player.target_y == self.y and self.dir == 2:
                    self.moving = False
                    self.walk_count = 0
                    player.dir = 3
                    self.initial_collide = True
                if player.target_x == self.x + TILESIZE and player.target_y == self.y and self.dir == 3:
                    self.moving = False
                    self.walk_count = 0
                    player.dir = 2
                    self.initial_collide = True

                if self.initial_collide:
                    while (player.target_x != player.x or player.target_y != player.y):
                        waiting = True
                        player.update()
                        self.game.draw()
                    self.check_interactions()

    def textbox_check(self):
        if self.initial_collide == True:
            self.text = True
        else:
            self.text = False

    def check_interactions(self):
        #Check for Dialog/Shop/Quests etc.
        #Check Visibility
        player_visible = True
        if self.game.player.invisible:
            player_visible = False
            dialog = random.choice(['What was that??', 'Uh, hello...?', 'AHHH- I mean, who goes there?!'])
        #self.game.QuestHandler.check_quests()
        #Check Quests
        has_quest_dialog = False
        if player_visible:
            for quest in self.game.quests:
                if not quest.active and not quest.complete and quest.check_prereqs():
                    if quest.giver == self.name:
                        dialog = quest.activate_quest()
                        has_quest_dialog = True
                elif quest.active and self.name in quest.activeSpeakers and not quest.complete:
                    if quest.has_dialog(self.name):
                        dialog = quest.get_quest_dialog(self.name)
                        has_quest_dialog = True
        #Random Dialog
        if player_visible and not has_quest_dialog:
            dialog = self.get_npc_dialog()

        #Draw textbox
        self.draw_dialog(dialog)
        #self.game.textbox.close_box()

    def get_npc_dialog(self):
        if not self.introduced:
            print('Introduction dialog')
            dialog = f"Hi I'm {self.name}"
            #self.game.STATE_DICT['text'].draw_dialog(self.name, dialog)
            self.introduced = True
        elif self.name in Special_NPCs:
            print('Special Dialog')
            dialog = 'I am a special NPC I will spawn here every time!'
        else:
            print('Generic dialog')
            dialog = f"I'm not important. This is a really long string that won't fit in the textbox unless we wrap it. So I made a text wrap func and going to try it out with this string. If a string is really really really long it might go on to the next page and my function should be able to hande that as well. The font is small so there has to be a lot of words in order to need mulitple pages, but if there is a monologue it may be useful. This last sentence should now be long enough that you will have to see a second page."
        return dialog

    def get_image(self):
        self.images[self.dir][self.walk_count // 6].blit(self.hair[self.dir], (0,0))
        self.image = self.images[self.dir][self.walk_count // 6]

    def draw(self, game):
        game.screen.blit(self.image, self.game.camera.apply(self))
        for item in [self.hat, self.pants, self.shirt, self.cloak, self.wand]:
            if item != None:
                game.screen.blit(item.images[self.dir][self.walk_count // 6], self.game.camera.apply(self))

    def draw_dialog(self, dialog):
        #Allow NPC to turn before textbox is open
        self.game.all_sprites.update()
        #Handle Text
        self.game.STATE_DICT['text'].draw_dialog(self.name, dialog)

    def wait_for_key_up(self):
        state = self.game.current_state
        self.game.state = 'waiting'
        hit_space = False
        while not hit_space:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    #next
                    if event.key == pg.K_SPACE:
                        hit_space = True
        self.game.current_state = state

    def get_npc_attribute(self, attr):
        if self.name_id in Special_NPCs:
            return Special_NPCs[self.name_id][attr]
        else:
            return self.generator.data_dict[attr]

    def check_if_special_npc(self, name):
        if name in Special_NPCs:
            return None
        else:
            return RandomNPCDataGenerator()

    def update(self):
        self.find_path()
        self.collides()
        self.move()
        self.get_image()
        self.rect.x = self.x
        self.rect.y = self.y

class Walk_Path(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, path_id):
        self.groups = game.walk_paths
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y
        self.path_id = path_id

class Textbox():
    def __init__(self, game, x, y):
        #self.groups = game.all_sprites, game.textbox
        #pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((0,0))
        self.image.fill(WHITE)
        self.width = 600
        self.height = 100
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, 300, 100)
        self.rect.x = x
        self.rect.y = y
        self.open = False

    def draw_box(self):
        self.image = pg.Surface((self.width,self.height))
        self.image.fill(WHITE)

    def close_box(self):
        self.image = pg.Surface((0,0))

    def update(self):
        pass

class SideMenu():
    def __init__(self, game):
        #self.groups = game.all_sprites, game.textbox
        #pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width = SIDE_MENU_W
        self.height = SIDE_MENU_H
        self.image = pg.Surface((self.width,self.height))
        self.image.fill(WHITE)
        self.font = pg.font.Font('freesansbold.ttf', 12)

    def clear(self):
        self.image.fill(WHITE)

class MenuItem():
    def __init__(self, game):
        #self.groups = game.all_sprites, game.textbox
        #pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width = SIDE_MENU_W
        self.height = SIDE_MENU_H
        self.image = pg.Surface((self.width,self.height))
        self.image.fill(WHITE)
        self.font = pg.font.Font('freesansbold.ttf', 12)

class Gate(pg.sprite.Sprite, LockedItem):
    def __init__(self, game, x, y, w, h, level, locked):
        super().__init__()
        self.groups = game.gates, game.interactables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        ### Surface and Collision Rect ###
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #Gate info
        self.level = level
        self.locked = locked
        self.open_image =  pg.image.load(path.join(img_folder, 'open_gate.png'))
        self.closed_image =  pg.image.load(path.join(img_folder, 'closed_gate.png'))

    def get_image(self):
        if self.locked:
            self.image = self.closed_image
        elif not self.locked:
            self.image = self.open_image

    def check_interactions(self):
        if self.locked:
            text = 'The gate is locked.'
            #Handle Text
            self.game.STATE_DICT['text'].draw_text(text)
        elif not self.locked:
            text = 'The gate is open.'
            self.game.STATE_DICT['text'].draw_text(text)

    def draw(self, game):
        game.screen.blit(self.image, game.camera.apply(self))

    def update(self):
        self.get_image()
