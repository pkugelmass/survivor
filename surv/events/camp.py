from .events import Event
from numpy.random import randint, choice

class Camp(Event):

    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = "Camp"
        self.time = 11

    def run(self,game):
        for tribe in game.tribes:
            for a in range(randint(1,3)):
                players = self.get_together(tribe)
                self.form_alliance(game,players)
                self.mark_complete()

    def get_together(self,tribe):
        size = randint(2,len(tribe.players)-1)
        players = choice(tribe.players,size=size,replace=False)
        return players

    def form_alliance(self,game,players):
        game.create_alliance(players)
        self.record('A new alliance has formed in {} among {}.', players[0].tribe, players)
