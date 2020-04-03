from .events import Event
from collections import Counter
from numpy.random import choice
from surv.utils.helpers import player_probabilities, choose_player

class TribalCouncil(Event):

    _formula = lambda player: 1/(player.strategy + player.social)

    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Tribal Council'
        self.votes = {}

    def run(self,game):
        self.participants = [x for x in game.tribes if not x.immunity][0].players
        self.record('Welcome, {}, to Tribal Council.', self.participants[0].tribe)
        self.record('{}... Light your torches.', self.participants)
        self.report_probabilities(player_probabilities(self.participants, TribalCouncil._formula)) #Event
        self.alliance_targets()
        self.vote()
        self.read_votes()
        self.announce_elmination()
        self.eliminate_player(game)
        self.mark_complete()

    def alliance_targets(self):
        alliances = list(set([p.alliance for p in self.participants if p.alliance != None and p.alliance.active==True]))
        for alliance in alliances:
            try:
                vulnerable_players = [p for p in self.participants if p.immunity == False]
                possible_targets = list(set(vulnerable_players) - set(alliance.members))
                alliance.target = choose_player(possible_targets, TribalCouncil._formula)
                self.record('{} is targeting {}.',alliance,alliance.target)
            except: # in the case where everyone is in the same alliance, somehow.
                self.record('There is no one for {} to target.', alliance)
                alliance.target = choose_player(alliance.members, TribalCouncil._formula)
                self.record('They turn on {}!',alliance.target)
                alliance.remove_player(alliance.target)

    def vote(self):
        self.record('It is... time to vote. {}, you\'re up...', choice(self.participants))
        for v in range(2):
            self.take_a_vote()
            if not self.votes_tied():
                return True

    def take_a_vote(self):
        for player in self.participants:
            if player.alliance == None:
                possible_targets = [p for p in self.participants if p != player and p.immunity == False]
                self.votes[player] = choose_player(possible_targets,TribalCouncil._formula)
            else:
                self.votes[player] = player.alliance.target

    def count_votes(self):
        return Counter(self.votes.values())

    def votes_tied(self):
        votes = self.count_votes()
        if len(votes) > 0:
            top2 = votes.most_common(2)
            if top2[0][1] != top2[1][1]:
                return False
        return True

    def draw_rocks(self):
        self.record('We are deadlocked. We will now draw rocks.')
        self.record('Reach into the bag and pull out a rock; white rock is eliminated.')
        self.result = choice([p for p in self.participants if p.immunity == False])
        self.record('Reveal... {} has drawn the white rock.',self.result)

    def read_votes(self):
        cnt = self.count_votes()
        self.record('I\'ll read the votes.')
        self.record(dict(cnt.most_common()))
        if not self.votes_tied():
            self.result = cnt.most_common(1)[0][0]
        else:
            self.draw_rocks()

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
        self.report_probabilities(player_probabilities(self.participants, TribalCouncil._formula)) #Event
        self.alliance_targets()
        self.vote()
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
        self.declare_winner(game)
        self.eliminate_runners_up(game) #TribalCouncil
        self.mark_complete()

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

    def declare_winner(self,game):
        self.record('The winner of Survivor... {}!', self.result)
        self.record('Let\'s see who voted for who: {}', self.votes)
        self.record('Thanks for a great season!')
        game.winner = self.result

    def eliminate_runners_up(self,game):
        for loser in self.participants[::-1]:
            if loser != self.result:
                game.eliminate(loser)
