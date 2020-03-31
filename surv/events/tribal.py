from .events import Event
from collections import Counter
from numpy.random import choice

class TribalCouncil(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Tribal Council'
        self.votes = {}

    def run(self,game):
        self.participants = [x for x in game.tribes if not x.immunity][0].players
        self.record('Welcome, {}, to Tribal Council.', self.participants[0].tribe)
        self.record('{}... Light your torches.', self.participants)
        vuln = self.calculate_vulnerability()
        self.report_probabilities(vuln) #Event
        self.vote(vuln)
        self.read_votes()
        self.announce_elmination()
        self.eliminate_player(game)
        self.mark_complete()

    def calculate_vulnerability(self):
        vulnerability = [1/(p.strategy + p.social) for p in self.participants]
        norm = [v/sum(vulnerability) for v in vulnerability]
        vuln = dict(zip(self.participants,norm))
        return vuln

    def vote(self,vulnerability):
        self.record('It is... time to vote. {}, you\'re up...', choice(self.participants))
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

    def announce_elmination(self):
        self.record('Next person voted off Survivor is {}; bring me your torch.', self.result)
        self.record('The tribe has spoken. It\'s time for you to go.')

    def eliminate_player(self,game):
        game.eliminate(self.result)

class JuryTribalCouncil(TribalCouncil):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Jury Tribal Council'

    def run(self,game):
        self.participants = game.active_players()
        self.record('Welcome, {}, to Tribal Council.', self.participants[0].tribe)
        self.record('{}... Light your torches.', self.participants)
        self.introduce_jury(game)
        self.announce_immunity(game)
        vuln = self.calculate_vulnerability() #TribalCouncil
        self.report_probabilities(vuln) #Event
        self.vote(vuln) #TribalCouncil
        self.read_votes() #TribalCouncil
        self.announce_elmination()
        self.eliminate_player(game) #TribalCouncil
        self.join_jury(game)
        self.mark_complete()

    def introduce_jury(self,game):
        if len(game.jury) > 0:
            self.record('Let\'s welcome the members of our jury, {}.', game.jury)

    def announce_immunity(self,game):
        if len(game.jury) > 0:
            immune = [x for x in self.participants if x.immunity][0]
            self.record('{} has immunity and is safe tonight.',immune)

    def join_jury(self,game):
        game.jury.append(self.result)
        self.record('{} will now join the jury.',self.result)

class FinalTribal(JuryTribalCouncil):

    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Final Tribal Council'

    def run(self,game):
        self.jury = game.jury
        self.participants = game.active_players()
        self.record('{}, you have made it {} days to get to this moment.',self.participants,game.parameters['days'])
        self.remove_immunity()
        self.introduce_jury(game)
        self.record('Jury, tonight you will vote FOR a winner.')
        strength = self.calculate_strength() #FinalTribal
        self.report_probabilities(strength) #Event
        self.vote(strength) #FinalTribal
        self.read_votes() #TribalCouncil
        self.declare_winner()
        self.eliminate_runners_up(game) #TribalCouncil
        self.mark_complete()
        self.end_game(game)

    def remove_immunity(self):
        for player in self.participants:
            player.immunity = False

    def calculate_strength(self):
        strength = [(p.strategy + p.social) for p in self.participants]
        norm = [float(v)/sum(strength) for v in strength]
        strength_dict = dict(zip(self.participants,norm))
        return strength_dict

    def vote(self,strength):
        while self.votes_tied():
            for player in self.jury:
                vote = None
                while vote == None:
                    my_vote = choice(list(strength.keys()),p=list(strength.values()))
                    if my_vote != player and my_vote.immunity == False:
                        vote = my_vote
                self.votes[player] = my_vote

    def declare_winner(self):
        self.record('The winner of Survivor... {}!', self.result)
        self.record('Let\'s see who voted for who: {}', self.votes)
        self.record('Thanks for a great season!')

    def eliminate_runners_up(self,game):
        for loser in self.participants[::-1]:
            if loser != self.result:
                game.eliminate(loser)

    def end_game(self,game):
        game.gameon = False
