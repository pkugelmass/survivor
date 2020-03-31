from .events import Event
from collections import Counter
from numpy.random import choice

class TribalCouncil(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Tribal Council'
        self.votes = {}
        self.jury = []

    def run(self,game):
        self.participants = [x for x in game.tribes if not x.immunity][0].players
        self.record('Welcome to Tribal Council, {}.', self.participants)
        self.record('Light your torches...')
        vuln = self.calculate_vulnerability()
        self.report_probabilities(vuln) #Event
        self.vote(vuln)
        self.read_votes()
        self.eliminate_player(game)
        self.mark_complete()

    def calculate_vulnerability(self):
        vulnerability = [1/(p.strategy + p.social) for p in self.participants]
        norm = [v/sum(vulnerability) for v in vulnerability]
        vuln = dict(zip(self.participants,norm))
        return vuln

    def vote(self,vulnerability):
        self.record('It is... time to vote. {}, you\'re up...', self.participants[0].first)
        while self.votes_tied():
            for player in self.participants:
                vote = None
                while vote == None:
                    my_vote = choice(list(vulnerability.keys()),p=list(vulnerability.values()))
                    if my_vote != player and my_vote.immunity == False:
                        vote = my_vote
                self.votes[player] = my_vote

    def count_votes(self):
        return Counter(self.votes.values())

    def votes_tied(self):
        votes = self.count_votes()
        if len(votes) > 0:
            top2 = votes.most_common(2)
            if top2[0][1] != top2[1][1]:
                return False
        return True

    def read_votes(self):
        cnt = self.count_votes()
        self.record('I\'ll read the votes.')
        self.record(dict(cnt.most_common()))
        self.result = cnt.most_common(1)[0][0]
        self.record('Next person voted off Survivor is {}; bring me your torch.', self.result.first)
        self.record('The tribe has spoken. It\'s time for you to go.')

    def eliminate_player(self,game):
        game.eliminate(self.result)

class JuryTribalCouncil(TribalCouncil):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Jury Tribal Council'

    def introduce_jury(self,game):
        if len(game.jury) > 0:
            self.jury = game.jury
            self.record('Let\'s welcome the members of our jury, {}.', self.jury)

    def start(self):
        if len(self.jury) > 0:
            self.record('Let\'s welcome the members of our jury: {}.'.format(self.jury))
        immune = [x for x in self.who if x.immunity][0]
        self.record('{} has immunity and is safe tonight.'.format(immune))

    def game_changes(self,game):
        game.jury.append(self.result)
        self.record('{} will now join the jury.'.format(self.result.first))

class FinalTribal(JuryTribalCouncil):

    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Final Tribal Council'

    def start(self):
        for player in self.who:
            player.immunity = False
        self.record('Let\'s welcome the members of our jury: {}.'.format(self.jury))
        self.record('Tonight you will vote FOR a winner.')

    def middle(self):
        while self.votes_tied():
            for player in self.jury:
                vote = None
                while vote == None:
                    my_vote = choice(self.who)
                    if my_vote != player and my_vote.immunity == False:
                        vote = my_vote
                self.votes[player] = my_vote

    def end(self):
        cnt = self.count_votes()
        self.record('I\'ll read the votes.')
        self.record(cnt.most_common())
        self.result = cnt.most_common(1)[0][0]
        self.record('The winner of Survivor... {}!'.format(self.result.first))
        self.record('Let\'s see who voted for who: {}'.format(self.votes))
        self.record('Thanks for a great season!')
        for loser in self.who[::-1]:
            if loser != self.result:
                loser.tribe.eliminate(loser)

    def game_changes(self,game):
        print('final game changes')
        game.gameon = False
