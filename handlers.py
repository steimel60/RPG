from settings import *
from items import *

class ItemHandler():
    def __init__(self, game):
        self.game = game
        self.galleons = 0
        self.sickles = 0
        self.knuts = 0
        self.inventory = []
        self.equipped = []

    def do_action(self, item, action):
        if action == 'Learn Spell':
            item.learn_spell(self.game)
            self.remove_item_by_action(item)
        if action == 'Destroy':
            self.remove_item_by_action(item)

    def remove_item_by_action(self, item):
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].inv_state = 'inventory'
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].act_box_sel_count = 0
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].selection = False
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].selection_count = 0
        self.game.player.inventory.remove(item)

class QuestHandler():
    pass

class SpellHandler():
    def __init__(self, game):
        self.game = game
        self.known_spells = []

    def learn_spell(self, spell):
        self.known_spells.append(spell)

    def cast(self, spell):
        item = self.get_item_to_cast_on()
        if item != None:
            spell.cast(item)

    def get_item_to_cast_on(self):
        player_x = self.game.player.x
        player_y = self.game.player.y
        if self.game.player.dir == 0: #Down
            for sprite in self.game.all_sprites:
                if sprite.x == player_x and sprite.y == player_y + TILESIZE:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 1: #Up
            for sprite in self.game.all_sprites:
                if sprite.x == player_x and sprite.y == player_y - TILESIZE:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 2: #Left
            for sprite in self.game.all_sprites:
                if sprite.x == player_x + TILESIZE and sprite.y == player_y:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 3: #Right
            for sprite in self.game.all_sprites:
                if sprite.x == player_x + TILESIZE and sprite.y == player_y:
                    if isinstance(sprite, Item):
                        return sprite
        else:
            return None
