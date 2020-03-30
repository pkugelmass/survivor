from .events import Event
from .tribal import TribalCouncil
from numpy.random import sample, choice
from numpy import mean

class Challenge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 12

    def run_challenge(self):
        self.result = choice(self.participants)

class TribalMixin:

    def equalize_tribes(self):
        bench = {tribe:[] for tribe in self.participants}
        sizes = [len(x.players) for x in self.participants]
        if max(sizes) != min(sizes):
            for tribe in self.participants:
                sit_out = len(x.players) - min(sizes)
                if sit_out > 0:
                    self.record('{} has to sit out {} players.'.format(tribe,sit_out))
                    sit_outs = sample(tribe.players,sit_out)
                    bench[tribe] = sit_outs
                    self.record('{} will sit out for {}; take a seat on the bench.'.format(sit_outs,tribe))
        return bench

    def calculate_strength(self, bench):
        tribestrengths = []
        for tribe in self.participants:
            indstrength = [p.physical for p in tribe.players if p not in bench[tribe]]
            strength = mean(indstrength)
            tribestrengths.append(strength)
        relative = [float(x)/sum(tribestrengths) for x in tribestrengths]
        strengths = dict(zip(self.participants,relative))
        self.record('Relative strengths: {}'.format(strengths))
        return strengths

    def run_challenge(self,strength):
        self.result = choice(list(strength.keys()),p=list(strength.values()))


class TribalReward(TribalMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Reward'

    def run(self,game):
        self.participants = game.tribes
        self.record('You ready for a reward challenge?')
        self.record('Getting a look at our tribes, {}.'.format(self.participants))
        sit_outs = self.equalize_tribes() #TribalMixin
        strengths = self.calculate_strength(sit_outs) #TribalMixin
        self.run_challenge(strengths) #TribalMixin
        self.announce_winner() #TribalReward
        self.mark_complete() #Event

    def announce_winner(self):
        losers = [x for x in self.participants if self.result != x]
        self.record('{} wins reward!'.format(self.result))
        self.record('{}, go back to camp; got nothin\' for ya.'.format(losers))

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

class TribalImmunity(Challenge):
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
