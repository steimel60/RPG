from items import *

class Quest():
    def __init__(self):
        self.active = False
        self.step_tracker = None

class TalkToEverybody(Quest):
    def __init__(self):
        self.name = 'Talk to Everybody'
        self.current_step = 'Activate'

    def feedback_dict(self):
        self.step_tracker = {
                'Activate':{'Prereqs': None,
                            'Dialog':{'Logan':'Go talk to DJ and Loren'},
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
        self.game = game
        self.active = False
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
            #self.game.textbox.draw_box()
            #self.game.textbox.draw_dialogue(self.giver, self.initialDialog)
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
        if name == 'DJ' and self.active and not self.talkedToDJ:
            dialog = self.talk_to_dj()
        elif name == 'Logan' and self.active and not self.talkedToDJ:
            dialog = self.logan_in_progress_dialog()
        elif name == 'Logan' and self.talkedToDJ:
            dialog = self.logan_quest_complete()

        return dialog

    def has_dialog(self, name):
        return name in self.activeSpeakers
    #Quest Specific
    def talk_to_dj(self):
        dialog = f"Hm.. I wonder what Logan wants"
        #self.game.textbox.draw_box()
        #self.game.textbox.draw_dialogue('DJ', dialog)
        self.talkedToDJ = True
        self.activeSpeakers = ['Logan']
        return dialog

    def logan_in_progress_dialog(self):
        dialog = f"You still need to find DJ"
        #self.game.textbox.draw_box()
        #self.game.textbox.draw_dialogue('Logan', dialog)
        return dialog

    def logan_quest_complete(self):
        dialog = f"Thanks! Take this chocolate frog card."
        #self.game.textbox.draw_box()
        #self.game.textbox.draw_dialogue('Logan', dialog)
        self.game.ItemHandler.add_item_to_inventory(ChocolateFrogCard('Neville Longbottom'))
        self.complete = True
        return dialog

class TradeWithLoren(Quest):
    def __init__(self, game):
        self.game = game
        self.active = False
        self.name = 'Trade Cards'
        self.prereqs = None
        self.giver = 'Loren'
        self.activeSpeakers = [self.giver]
        self.initialDialog = 'Is that a chocolate frog?'
        self.complete = False
        ### Steps ###
        self.tradedCard = False
    #General Funcs
    def activate_quest(self):
        if self.check_prereqs():
            self.active = True
            self.game.textbox.draw_box()
            self.game.textbox.draw_dialogue(self.giver, self.initialDialog)
            self.activeSpeakers = ['Loren']

    def check_prereqs(self):
        prereqs_met = any(isinstance(x, ChocolateFrogCard) for x in self.game.ItemHandler.inventory)
        return prereqs_met

    def get_quest_dialog(self, name):
        if name == 'Loren' and self.active and not self.tradedCard:
            self.be_asked_to_trade()
            return self.has_dialog()

    def has_dialog(self):
        return True
    #Quest Specific
    def be_asked_to_trade(self):
        dialog = "Let's trade cards!"
        self.game.textbox.draw_box()
        self.game.textbox.draw_dialogue('Loren', dialog)
        self.talkedToDJ = True
        self.activeSpeakers = ['Loren']
