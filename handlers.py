from settings import *
from items import *

#Handlers are used to track and handle data that needs to remain consistent between level loads

class ItemHandler():
    def __init__(self, game):
        self.game = game
        self.galleons = 0
        self.sickles = 2
        self.knuts = 12
        self.inventory = test_inventory
        self.equipped = []
        self.inventory_length = len(self.inventory) + len(self.equipped)

    def add_item_to_inventory(self, item):
        self.inventory.append(item)
        self.inventory_length += 1

    def equip_item(self, item):
        for equipped_item in self.equipped:
            if type(equipped_item) == type(item):
                self.unequip_item(equipped_item)
        self.equipped.append(item)
        self.inventory.remove(item)

        item.equip_effect(self.game)
        #Change actions for inventory
        item.actions = list(map(lambda action: action.replace("Equip","Unequip"), item.actions))
        #Change alpha if invisible
        if isinstance(item, Wearable) and self.game.player.invisible:
            for img_list in item.images:
                for img in img_list:
                    img.set_alpha(100)

    def unequip_item(self, item):
        self.inventory.append(item)
        self.equipped.remove(item)
        item.unequip_effect(self.game)
        item.actions = list(map(lambda action: action.replace("Unequip","Equip"), item.actions))
        #reset alpha if changed
        if isinstance(item, Wearable) and self.game.player.invisible:
            for img_list in item.images:
                for img in img_list:
                    img.set_alpha(255)

    def do_action(self, item, action):
        if action == 'Learn Spell':
            item.learn_spell(self.game)
            self.remove_item_by_action(item)
        elif action == 'Destroy':
            self.remove_item_by_action(item)
        elif action == 'Equip':
            self.close_action_box()
            self.equip_item(item)
        elif action == 'Unequip':
            self.close_action_box()
            self.unequip_item(item)

    def close_action_box(self):
        #Close Action Box and Return to Inventory Menu
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].inv_state = 'inventory'
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].act_box_sel_count = 0
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].selection = False
        self.game.STATE_DICT['menu'].menu_dict['Inventory'].selectionCount = 0

    def remove_item_by_action(self, item):
        self.close_action_box()
        #Remove Item
        self.inventory.remove(item)
        self.inventory_length -= 1

class QuestHandler():
    def __init__(self, game):
        self.game = game
        self.active_quests = []
        self.completed_quests = []

    def activate_quest(self, quest):
        self.active_quests.append(quest)

    def check_step_prereqs(self, quest):
        if quest.step_tracker[quest.current_step]['Prereqs'] == None:
            return True
        return all(quest.step_tracker[quest.current_step])

class SpellHandler():
    def __init__(self, game):
        self.game = game
        self.known_spells = []

    def learn_spell(self, spell):
        self.known_spells.append(spell)

    def cast(self, spell):
        item = self.get_item_to_cast_on()
        if item != None:
            #Check that a wand is equipped
            if any(isinstance(item, Wand) for item in self.game.ItemHandler.equipped):
                spell.cast(item)
                text = f'{spell.name}!'
                self.game.STATE_DICT['text'].draw_text(text)
            else:
                text = 'You must have a wand equipped to cast spells!'
                self.game.STATE_DICT['text'].draw_text(text)

    def get_item_to_cast_on(self):
        player_x = self.game.player.x
        player_y = self.game.player.y
        if self.game.player.dir == 0: #Down
            for sprite in self.game.interactables:
                if sprite.x == player_x and sprite.y == player_y + 2*TILESIZE:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 1: #Up
            for sprite in self.game.interactables:
                if sprite.x == player_x and sprite.y == player_y:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 2: #Left
            for sprite in self.game.interactables:
                if sprite.x == player_x + TILESIZE and sprite.y == player_y:
                    if isinstance(sprite, Item):
                        return sprite
        elif self.game.player.dir == 3: #Right
            for sprite in self.game.interactables:
                if sprite.x == player_x + TILESIZE and sprite.y == player_y:
                    if isinstance(sprite, Item):
                        return sprite
        else:
            return None
