from .events import Event
from collections import Counter
from random import choice

class TribalCouncil(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Tribal Council'
        self.votes = {}
        self.jury = []

    def find_participants(self,game):
        tribe = list(filter(lambda x: x.immunity == False, game.tribes))[0]
        self.who = tribe.players
        if len(game.jury) > 0:
            self.jury = game.jury

    def count_votes(self):
        return Counter(self.votes.values())

    def votes_tied(self):
        votes = self.count_votes()
        if len(votes) > 0:
            top2 = votes.most_common(2)
            if top2[0][1] != top2[1][1]:
                return False
        return True

    def start(self):
        self.record('Light your torches...')

    def middle(self):
        while self.votes_tied():
            for player in self.who:
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
        self.record('Next person voted off Survivor is {}; bring me your torch.'.format(self.result.first))
        self.record('The tribe has spoken. It\'s time for you to go.')
        self.result.tribe.eliminate(self.result)

class JuryTribalCouncil(TribalCouncil):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Jury Tribal Council'

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
