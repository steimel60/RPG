import pygame as pg
from settings import *
from items import *
from dialouges import *
from specialNPCs import *
from blanks import change_color, img_folder, game_folder, walk_up_img, walk_down_img, walk_left_img, walk_right_img, hair_list, hairColors
from os import path
import random

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
        if self.moving and not self.collides():
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

    def collide_with_walls(self):
        for wall in self.game.walls:
            if wall.x <= self.target_x <= (wall.x + wall.w-TILESIZE) and wall.y <= self.target_y <= (wall.y + wall.h-TILESIZE):
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
                if gate.x <= self.target_x <= (gate.x + gate.w-TILESIZE) and gate.y <= self.target_y <= (gate.y + gate.h-TILESIZE):
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
        for item in [self.hat, self.shirt, self.cloak, self.wand]:
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
                if interactable.x == self.x and interactable.y == self.y - TILESIZE:
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
    def __init__(self, game, dir, x, y, path_id, name, skin_id, hair_id, hair_color):
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
        ### Movement Control ###
        self.moving = False
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.walk_count = 0
        self.dir = dir
        self.path_id = path_id
        self.initial_collide = False
        self.collide_wait = False
        self.text = False
        ### Unique IDs ###
        self.name = name
        self.introduced = False
        #Wearables
        self.hat = None
        self.cloak = None
        self.shirt = None
        self.pants = None
        self.wand = None

    def move(self):
        if self.walk_count + 1 > 23:
            self.walk_count = 0
        if self.moving:
            """
            move by 4 pixles until reaching target x,y
            """
            self.initial_collide = False
            self.collide_wait = True  ## Player has moved since first colliding
            if self.target_x > self.x: #right
                self.x += WALK_SPEED
                self.walk_count += 1
                self.dir = 3
            if self.target_x < self.x: #left
                self.x -= WALK_SPEED
                self.walk_count += 1
                self.dir = 2
            if self.target_y > self.y: #down
                self.y += WALK_SPEED
                self.walk_count += 1
                self.dir = 0
            if self.target_y < self.y: #up
                self.y -= WALK_SPEED
                self.walk_count += 1
                self.dir = 1
        else:
            if self.moving_up:
                self.dir = 1
            if self.moving_down:
                self.dir = 0
            if self.moving_left:
                self.dir = 2
            if self.moving_right:
                self.dir = 3

    def find_path(self):
        if self.path_id != -1:
            for path in self.game.walk_paths:
                if path.path_id == self.path_id:
                    current_path = path
                """
                Check if path is vertical or horizontal, npc is width of tile that's why we compare width and height to tile size
                right now path is either 1 tile wide or tall, then extended in other direction
                """
            if current_path.w > TILESIZE:
                if self.x == current_path.x: #if at left of path move right
                    self.target_x = current_path.x + current_path.w
                    self.moving_right = True
                    self.moving_left = False
                if self.x == current_path.x + current_path.w: #if at right of path move left
                    self.target_x = current_path.x
                    self.moving_left = True
                    self.moving_right = False
            if current_path.h > TILESIZE:
                if self.y == current_path.y: #when at top of path move down
                    self.target_y = current_path.y + current_path.h
                    self.moving_down = True
                    self.moving_up = False
                if self.y == current_path.y + current_path.h: #when at bottom of path move up
                    self.target_y = current_path.y
                    self.moving_up = True
                    self.moving_down = False
            if not self.moving:
                self.moving = True
                if self.moving_up:
                    self.target_y = current_path.y
                elif self.moving_down:
                    self.target_y = current_path.y + current_path.h
                elif self.moving_left:
                    self.target_x = current_path.x
                elif self.moving_right:
                    self.target_x = current_path.x + current_path.w
                else:
                    self.target_x = current_path.x
                    self.target_y = current_path.y

    def collides(self):
        for player in self.game.user_group:
            if player.target_x == self.x and player.target_y == self.y + TILESIZE and self.moving_down:
                self.moving = False
                self.walk_count = 0
                player.dir = 1
                self.initial_collide = True
            if player.target_x == self.x and player.target_y == self.y - TILESIZE and self.moving_up:
                self.moving = False
                self.walk_count = 0
                player.dir = 0
                self.initial_collide = True
            if player.target_x == self.x - TILESIZE and player.target_y == self.y and self.moving_left:
                self.moving = False
                self.walk_count = 0
                player.dir = 3
                self.initial_collide = True
            if player.target_x == self.x + TILESIZE and player.target_y == self.y and self.moving_right:
                self.moving = False
                self.walk_count = 0
                player.dir = 2
                self.initial_collide = True

    def textbox_check(self):
        if self.initial_collide == True:
            self.text = True
        else:
            self.text = False

    def check_interactions(self):
        #Check for Dialog/Shop/Quests etc.
        #Check Quests
        player_visible = True
        if self.game.player.invisible:
            player_visible = False
            text = random.choice(['What was that??', 'Uh, hello...?', 'AHHH- I mean, who goes there?!'])
            self.game.textbox.draw_box()
            self.game.textbox.draw_dialogue(self.name, text)
        #self.game.QuestHandler.check_quests()
        has_quest_dialog = False
        if player_visible:
            for quest in self.game.quests:
                if not quest.active and not quest.complete and quest.check_prereqs():
                    if quest.giver == self.name:
                        quest.activate_quest()
                        has_quest_dialog = True
                elif quest.active and self.name in quest.activeSpeakers and not quest.complete:
                    if quest.get_quest_dialog(self.name):
                        has_quest_dialog = True
        #Random Dialog
        if player_visible and not has_quest_dialog:
            self.get_npc_dialog()

    def get_npc_dialog(self):
        if not self.introduced:
            dialog = f"Hi I'm {self.name}"
            self.game.textbox.draw_box()
            self.game.textbox.draw_text(dialog)
            self.introduced = True
        elif self.name in Special_NPCs:
            topic = random.choice(list(Special_NPCs[self.name].keys()))
            if topic == 'House':
                dialog = random.choice([f"I'm in {Special_NPCs[self.name][topic]}!", f"{Special_NPCs[self.name][topic]} is the best house at Hogwarts!"])
            elif topic == 'Pet':
                dialog = random.choice([f"I just got a pet {Special_NPCs[self.name][topic]}!", f"My {Special_NPCs[self.name][topic]}'s name is {self.name} Jr."])
            self.game.textbox.draw_box()
            self.game.textbox.draw_text(dialog)
        else:
            dialog = f"I'm not important"
            self.game.textbox.draw_box()
            self.game.textbox.draw_text(dialog)

    def get_image(self):
        self.images[self.dir][self.walk_count // 6].blit(self.hair[self.dir], (0,0))
        self.image = self.images[self.dir][self.walk_count // 6]

    def draw(self, game):
        game.screen.blit(self.image, self.game.camera.apply(self))
        for item in [self.hat, self.shirt, self.cloak, self.wand]:
            if item != None:
                game.screen.blit(item.images[self.dir][self.walk_count // 6], self.game.camera.apply(self))

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
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, 300, 100)
        self.rect.x = x
        self.rect.y = y

    def draw_box(self):
        self.image = pg.Surface((600,100))
        self.image.fill(WHITE)

    def draw_text(self, dialog):
        font = pg.font.Font('freesansbold.ttf', 16)
        text = font.render(dialog, True, BLACK, WHITE)
        textRect = text.get_rect()
        self.image.blit(text, textRect)

    def check_game(self):
        for user in self.game.user_group:
            if user.moving:
                self.close_box()

    def draw_dialogue(self, name, dialog):
        font = pg.font.Font('freesansbold.ttf', 16)
        text = font.render(f'{name}: {dialog}', True, BLACK, WHITE)
        textRect = text.get_rect()
        self.image.blit(text, textRect)

    def yes_no_question(self, name, question, answer):
        font = pg.font.Font('freesansbold.ttf', 16)
        self.draw_dialogue(name, question)
        #Get fonts and sizes
        yes_font = font.render(f'Yes', True, BLACK, WHITE)
        no_font = font.render(f'No', True, BLACK, WHITE)
        arrow_font = font.render(f' <-', True, BLACK, WHITE)
        q_size = font.size(f'{name}: {question}')
        y_size = font.size('Yes')
        n_size = font.size('No')
        arrow_size = font.size(' <-')
        #Get Font Locations
        y_loc = (0,q_size[1])
        n_loc = (0,y_loc[1]+y_size[1])
        if answer == 'yes':
            arrow_loc = (y_size[0],y_loc[1])
        else:
            arrow_loc = (n_size[0],n_loc[1])
        #blit to textbox
        self.image.blit(yes_font, y_loc)
        self.image.blit(no_font, n_loc)
        self.image.blit(arrow_font, arrow_loc)
    def get_text(self, text):
        #Read in text to display as a list (pages)
        pass

    def close_box(self):
        self.image = pg.Surface((0,0))

    def update(self):
        self.check_game()

class SideMenu():
    def __init__(self, game):
        #self.groups = game.all_sprites, game.textbox
        #pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((300,600))
        self.image.fill(WHITE)
        self.font = pg.font.Font('freesansbold.ttf', 12)

    def clear(self):
        self.image.fill(WHITE)

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
            self.game.textbox.draw_box()
            self.game.textbox.draw_text(text)
        elif not self.locked:
            text = 'The gate is open.'
            self.game.textbox.draw_box()
            self.game.textbox.draw_text(text)

    def draw(self, game):
        game.screen.blit(self.image, game.camera.apply(self))

    def update(self):
        self.get_image()
