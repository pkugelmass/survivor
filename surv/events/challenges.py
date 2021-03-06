from .events import Event, htmlify
from .tribal import TribalCouncil
from numpy.random import sample, choice
from numpy import mean

class Challenge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 12

    def run_challenge(self,strength):
        self.result = choice(list(strength.keys()),p=list(strength.values()))

class RewardMixin:

    def announce_winner(self):
        losers = [x for x in self.participants if self.result != x]
        self.record('{} wins reward!', self.result)
        self.record('{}, go back to camp; got nothin\' for ya.', losers)

class TribalMixin:

    def equalize_tribes(self):
        bench = {tribe:[] for tribe in self.participants}
        sizes = [len(x.players) for x in self.participants]
        if max(sizes) != min(sizes):
            for tribe in self.participants:
                sit_out = len(tribe.players) - min(sizes)
                if sit_out > 0:
                    self.record('{} has to sit out {} players.', tribe, sit_out)
                    sit_outs = choice(tribe.players,size=sit_out)
                    bench[tribe] = sit_outs
                    self.record('{} will sit out for {}; take a seat on the bench.',sit_outs,tribe)
        return bench

    def calculate_strength(self, bench):
        tribestrengths = []
        for tribe in self.participants:
            indstrength = [p.physical for p in tribe.players if p not in bench[tribe]]
            strength = mean(indstrength)
            tribestrengths.append(strength)
        relative = [round(float(x)/sum(tribestrengths),3) for x in tribestrengths]
        strengths = dict(zip(self.participants,relative))
        return strengths

class ImmunityMixin:

    def take_back_immunity(self):
        taken_back = False
        for x in self.participants:
            if x.immunity == True:
                self.record('Immunity is back up for grabs.')
                x.immunity = False
                taken_back = True
        if not taken_back:
            self.record('This is what you\'re competing for: immunity.')

    def announce_winner(self):
        self.record('{} wins immunity!', self.result)
        losing_tribes = list(set(self.participants) - set([self.result]))
        self.record('{}, I\'ll see you at tribal council.', losing_tribes)

    def award_immunity(self):
        self.result.immunity = True

class IndividualMixin:

    def calculate_strength(self):
        strengths = [p.physical for p in self.participants]
        relative = [float(x)/sum(strengths) for x in strengths]
        strength_dict = dict(zip(self.participants,relative))
        return strength_dict

class TribalReward(TribalMixin, RewardMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Reward'

    def run(self,game):
        self.participants = game.tribes
        self.record('You ready for a reward challenge?')
        self.record('Getting a look at our tribes, {}.', self.participants)
        sit_outs = self.equalize_tribes() #TribalMixin
        strengths = self.calculate_strength(sit_outs) #TribalMixin
        self.report_probabilities(strengths) #Event
        self.run_challenge(strengths) #Event
        self.announce_winner() #RewardMixin
        self.mark_complete() #Event

class TribalImmunity(TribalMixin, ImmunityMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Immunity'

    def run(self,game):
        self.participants = game.tribes
        self.record('Getting a look at our tribes, {}.', self.participants)
        self.take_back_immunity() #ImmunityMixin
        sit_outs = self.equalize_tribes() #TribalMixin
        strengths = self.calculate_strength(sit_outs) #TribalMixin
        self.report_probabilities(strengths) #Event
        self.run_challenge(strengths) #Challenge
        self.announce_winner() #ImmunityMixin
        self.award_immunity() #ImmunityMixin
        self.mark_complete() #Event
        self.update_tribal(game)

    def update_tribal(self,game):
        going_to_tribal = [x for x in game.tribes if x.immunity == False][0]
        upcoming_tribal = list(filter(lambda x: not x.complete,game.schedule.event_type(TribalCouncil)))[0]
        upcoming_tribal.name = upcoming_tribal.name + ' ({})'.format(going_to_tribal.name)

class IndividualImmunity(IndividualMixin, ImmunityMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Immunity'

    def run(self,game):
        self.participants = game.active_players()
        self.record('Getting a look at our final {}, {}.', len(self.participants),self.participants)
        self.take_back_immunity() #ImmunityMixin
        strengths = self.calculate_strength() #IndividualMixin
        self.report_probabilities(strengths) #Event
        self.run_challenge(strengths) #Challenge
        self.announce_winner() #ImmunityMixin
        self.award_immunity() #ImmunityMixin
        self.mark_complete() #Event
        # self.update_tribal(game)

class IndividualReward(IndividualMixin, RewardMixin, Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Reward'

    def run(self,game):
        self.participants = game.active_players()
        self.record('You ready for a reward challenge?')
        self.record('Getting a look at our final {}, {}.', len(self.participants),self.participants)
        strengths = self.calculate_strength() #IndividualMixin
        self.report_probabilities(strengths) #Event
        self.run_challenge(strengths) #Challenge
        self.announce_winner() #RewardMixin
        self.mark_complete() #Event
