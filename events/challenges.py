from .events import Event
from .tribal import TribalCouncil

class Challenge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 12

class IndividualMixin():

    def find_participants(self,game):
        self.who = game.active_players()

class IndividualImmunity(IndividualMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Immunity'

    def start(self):
        for player in self.who:
            if player.immunity == True:
                self.record('I\'ll take the necklace back from {}.'.format(player))
                self.record('Individual immunity is back up for grabs.')
                player.immunity = False

    def end(self):
        self.result.immunity = True
        self.record('{} wins immunity!'.format(self.result.first))

class IndividualReward(IndividualMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Reward'



class TribesMixin:
    def find_participants(self,game):
        self.who = game.tribes

class TribalImmunity(TribesMixin,Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Immunity'

    def start(self):
        for tribe in self.who:
            if tribe.immunity == True:
                self.record('Immunity is back up for grabs.')
                tribe.immunity = False

    def end(self):
        self.record('{} wins immunity!'.format(self.result))
        self.result.immunity = True
        losing_tribes = list(set(self.who) - set([self.result]))
        self.record('{}, I\'ll see you at tribal council.'.format(losing_tribes))

    def game_changes(self,game):
        self.complete = True
        going_to_tribal = [x for x in game.tribes if x.immunity == False][0]
        upcoming_tribal = list(filter(lambda x: not x.complete,game.schedule.event_type(TribalCouncil)))[0]
        upcoming_tribal.name = upcoming_tribal.name + ' ({})'.format(going_to_tribal.name)

class TribalReward(TribesMixin,Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Reward'

    def end(self):
        self.record('{} wins reward!'.format(self.result))
        losing_tribes = list(set(self.who) - set([self.result]))
        self.record('{}, head back to camp; got nothin\' for ya.'.format(losing_tribes))
