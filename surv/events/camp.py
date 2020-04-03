from .events import Event
from numpy.random import randint, choice, normal
from itertools import permutations

class Camp(Event):

    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = "Camp"
        self.time = 11

    def run(self,game):
        for tribe in game.tribes:
            self.camp_talk(tribe.players)


            for a in range(randint(1,3)):
                players = self.get_together(tribe)
                self.form_alliance(game,players)
                self.mark_complete()

    def camp_talk(self,players):
        for pair in permutations(players,2):
            p1, p2 = pair
            p2_mean = (p2.social-3) * 0.25
            p2_effect = normal(p2_mean,0.5)
            p1.relationships[p2] += p2_effect


    def get_together(self,tribe):
        size = randint(2,len(tribe.players)-1)
        players = choice(tribe.players,size=size,replace=False)
        return players

    def form_alliance(self,game,players):
        game.create_alliance(players)
        self.record('A new alliance has formed in {} among {}.', players[0].tribe, players)
