from items import *
from sprites import NPC

class Quest():
    def __init__(self, game):
        self.active = False
        self.game = game
        self.has_scene_by_map_load = False

    def has_dialog(self, name):
        return name in self.activeSpeakers

    def check_prereqs(self):
        prereqs_met = False
        for quest in self.game.quests:
            if quest.name in self.prereqs:
                if quest.complete == True:
                    prereqs_met = True
        if len(self.prereqs) == 0:
            prereqs_met = True
        return prereqs_met

class GetAWand(Quest):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Get a Wand"
        self.prereqs = []
        self.giver = 'Dad'
        self.active = True
        self.activeSpeakers = [self.giver]
        self.initialDialog = 'Here is some money son. Go get a wand from Wanda.'
        self.complete = False
        self.has_scene_by_map_load = True
        ### Steps ###
        self.talkedToDad = False
        self.findWanda = False
        self.toldGetScroll = False

    #General Funcs
    def quest_step_by_load(self):
        if self.talkedToDad == False and self.game.level == 'test':
            self.talk_to_dad()
        if self.game.level == 'indoor1':
            self.findWanda = True
        if self.findWanda == True and self.game.level == 'test' and self.toldGetScroll == False:
            if any([isinstance(x, Wand) for x in self.game.ItemHandler.inventory]):
                self.get_a_scroll()
    def get_quest_dialog(self, name):
        if self.check_prereqs() == False:
            return 'NODIALOG'
        #Do Quest
        if name == 'DJ' and self.active and not self.talkedToDJ:
            dialog = self.talk_to_dj()
        elif name == 'Logan' and self.active and not self.talkedToDJ:
            dialog = self.logan_in_progress_dialog()
        #Finish
        elif name == 'Logan' and self.talkedToDJ:
            dialog = self.logan_quest_complete()

        return dialog
    #Quest Specific
    def talk_to_dad(self):
        self.game.STATE_DICT['scene'].enter_scene_state()
        dad = NPC(self.game, dir = 2, x=self.game.player.x - TILESIZE*2, y=self.game.player.y + TILESIZE*6, name_id='Dad')
        dad.initial_collide = True
        dad.target_x = self.game.player.x
        while dad.target_x != dad.x:
            dad.moving = True
            dad.update()
            self.game.draw()
        dad.target_y = self.game.player.y + TILESIZE
        while dad.target_y != dad.y:
            dad.moving = True
            dad.update()
            self.game.draw()
        self.game.STATE_DICT['text'].draw_dialog(dad.name, self.initialDialog)
        dad.target_x -= TILESIZE*2
        while dad.target_x != dad.x:
            dad.moving = True
            dad.update()
            self.game.draw()
        dad.kill()
        self.game.STATE_DICT['scene'].exit_scene_state()
        self.talkedToDad = True

    def get_a_scroll(self):
        self.game.STATE_DICT['scene'].enter_scene_state()
        dad = NPC(self.game, dir = 2, x=self.game.player.x - TILESIZE*7, y=self.game.player.y + TILESIZE*6, name_id='Dad')
        dad.initial_collide = True
        dad.target_x = self.game.player.x
        while dad.target_x != dad.x:
            dad.moving = True
            dad.update()
            self.game.draw()
        dad.target_y = self.game.player.y + TILESIZE
        while dad.target_y != dad.y:
            dad.moving = True
            dad.update()
            self.game.draw()
        self.game.STATE_DICT['text'].draw_dialog(dad.name, "You're school supplies list also suggest purchasing an Alohamora Scroll. Dr. Booksy should have one of those!")
        dad.target_x -= TILESIZE*7
        while dad.target_x != dad.x:
            dad.moving = True
            dad.update()
            self.game.draw()
        dad.kill()
        self.game.STATE_DICT['scene'].exit_scene_state()
        self.toldGetScroll = True


class TalkToEverybody(Quest):
    def __init__(self):
        self.name = 'Talk to Everybody'
        self.current_step = 'Activate'

    def feedback_dict(self):
        self.step_tracker = {
                'Activate':{'Prereqs': None,
                            'Dialog':{'Logan':'Go talk to DJ and Loren'},
                            'Hint':'Find DJ and Loren'},
                'Main':{'Prereqs':[self.active],
                        'Dialog':{'Logan':'Go talk to DJ and Loren',
                                'DJ':'You are doing a quest?',
                                'Loren':'Ah my brother beckons me?'},
                        'Hint':'Find DJ and Loren'}
        }

    def update(self, interactable):
        if self.current_step == 'Activate' and interactable.name == 'Logan':
            self.active = True
        if name == 'DJ' and self.active and not self.talkedToDJ:
            self.talk_to_dj()
            return self.has_dialog()
        elif name == 'Logan' and self.active and not self.talkedToDJ:
            self.logan_in_progress_dialog()
            self.has_dialog()
            return self.has_dialog()
        elif name == 'Logan' and self.talkedToDJ:
            self.logan_quest_complete()
            self.has_dialog()
            return self.has_dialog()

class TestQuest(Quest):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Logan's Friend"
        self.prereqs = []
        self.giver = 'Logan'
        self.activeSpeakers = [self.giver]
        self.initialDialog = 'Go find DJ'
        self.complete = False
        ### Steps ###
        self.talkedToDJ = False
    #General Funcs
    def activate_quest(self):
        if self.check_prereqs():
            self.active = True
            self.activeSpeakers = ['Logan', 'DJ']
            return self.initialDialog

    def check_prereqs(self):
        prereqs_met = False
        for quest in self.game.quests:
            if quest.name in self.prereqs:
                if quest.complete == True:
                    prereqs_met = True
        if len(self.prereqs) == 0:
            prereqs_met = True
        return prereqs_met

    def get_quest_dialog(self, name):
        if self.check_prereqs() == False:
            return 'NODIALOG'
        #Do Quest
        if name == 'DJ' and self.active and not self.talkedToDJ:
            dialog = self.talk_to_dj()
        elif name == 'Logan' and self.active and not self.talkedToDJ:
            dialog = self.logan_in_progress_dialog()
        #Finish
        elif name == 'Logan' and self.talkedToDJ:
            dialog = self.logan_quest_complete()

        return dialog

    #Quest Specific
    def talk_to_dj(self):
        dialog = f"Hm.. I wonder what Logan wants"
        self.talkedToDJ = True
        self.activeSpeakers = ['Logan']
        return dialog

    def logan_in_progress_dialog(self):
        dialog = f"You still need to find DJ"
        return dialog

    def logan_quest_complete(self):
        dialog = f"Thanks! Take this chocolate frog card."
        self.game.ItemHandler.add_item_to_inventory(ChocolateFrogCard('Neville Longbottom'))
        self.complete = True
        return dialog

class TradeWithLoren(Quest):
    def __init__(self, game):
        super().__init__(game)
        self.name = 'Trade Cards'
        self.prereqs = None
        self.giver = 'Loren'
        self.activeSpeakers = [self.giver]
        self.initialDialog = 'Is that a chocolate frog?'
        self.complete = False
        ### Steps ###
        self.cardSpotted = False
    #General Funcs
    def activate_quest(self):
        if self.check_prereqs():
            self.active = True
            self.activeSpeakers = ['Loren']
            self.cardSpotted = True
            return self.initialDialog

    def check_prereqs(self):
        prereqs_met = any(isinstance(x, ChocolateFrogCard) for x in self.game.ItemHandler.inventory)
        return prereqs_met

    def get_quest_dialog(self, name):
        if name == 'Loren' and self.cardSpotted:
            dialog = self.be_asked_to_trade()
            self.complete = True
            self.active = False
        return dialog

    #Quest Specific
    def be_asked_to_trade(self):
        dialog = "Let's trade cards!"
        self.game.STATE_DICT['text'].draw_dialog('Loren', dialog)
        self.game.STATE_DICT['scene'].enter_scene_state()
        mom = NPC(self.game, dir = 2, x=self.game.player.x + TILESIZE*15, y=self.game.player.y, name_id='Mom')
        mom.initial_collide = True
        mom.target_x = self.game.player.x + TILESIZE
        while mom.target_x != mom.x:
            mom.moving = True
            mom.update()
            self.game.draw()
        self.game.STATE_DICT['text'].draw_dialog(mom.name, "Don't you dare trade with Loren, he will rip you off!!" )
        mom.target_x += TILESIZE*15
        while mom.target_x != mom.x:
            mom.moving = True
            mom.update()
            self.game.draw()
        mom.kill()
        self.game.STATE_DICT['scene'].exit_scene_state()
        self.activeSpeakers = ['Loren']
        dialog = "Nevermind..."
        return dialog

class LovePotion(Quest):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Love Potion"
        self.prereqs = []
        self.giver = 'Bryn'
        self.activeSpeakers = [self.giver]
        self.initialDialog = 'Hey I need some help!'
        self.complete = False
        ### Steps ###
        self.talkedToBryn = False
        self.gave_dylan_potion = False
    #General Funcs
    def activate_quest(self):
        if self.check_prereqs():
            self.active = True
            self.activeSpeakers = ['Bryn']
            return self.initialDialog

    def check_prereqs(self):
        prereqs_met = False
        for quest in self.game.quests:
            if quest.name in self.prereqs:
                if quest.complete == True:
                    prereqs_met = True
        if len(self.prereqs) == 0:
            prereqs_met = True
        return prereqs_met

    def get_quest_dialog(self, name):
        if self.check_prereqs() == False:
            return 'NODIALOG'
        #Do Quest
        if name == 'Bryn' and self.active and not self.talkedToBryn:
            dialog = self.talk_to_bryn()

        return dialog

    #Quest Specific
    def talk_to_bryn(self):
        dialog = f"I need you to find Dylan and give him this potion.."
        self.talkedToBryn = True
        self.activeSpeakers = ['Bryn']
        return dialog
