from .events import Event
from itertools import cycle
from numpy.random import shuffle,choice
import re

class Intro(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Introductions"

    def run(self,game):
        self.participants = game.tribes
        self.record('Welcome to another season of Survivor. Let\'s meet our players.')
        self.introduce_tribes()
        self.record('{} people... {} days... ONE SURVIVOR!',len(game.players),game.parameters['days'])
        self.mark_complete()

    def introduce_tribes(self):
        lead_ins = ['First','Next','Finally','Also','And wow']
        for i,tribe in enumerate(self.participants):
            self.record('{}, the {} tribe...',lead_ins[i],tribe)
            for p in tribe.players:
                self.record('-- {}, a {} year old {} from {}.',p,p.age,p.job,p.hometown)

class Merge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Merge"

    def run(self,game):
        self.participants = game.tribes
        self.record('{} are merging!'.format(self.participants))
        self.merge_tribes(game)
        self.mark_complete()

    def merge_tribes(self,game):
        new_name = self.new_tribe_name(game)
        [game.retire_tribe(t) for t in game.tribes[::-1]]
        self.record('The new tribe is called {}.'.format(new_name))
        merged_tribe = game.add_tribe(name=new_name)
        [merged_tribe.add_player(x) for x in game.active_players()]
        self.record('Let\'s have a look at the new tribe.')
        self.record({x:x.players for x in self.participants})
        self.result = merged_tribe

    def new_tribe_name(self,game):
        names = [t.name for t in game.tribes]
        justletters = re.sub('\s','',''.join(names))
        syllables = re.findall('[^aeiouAEIOU]+[aeiou]',justletters)
        num_syllables = choice(range(2,len(syllables)))
        new_word = ''.join(choice(syllables,num_syllables,replace=False)).title()
        return new_word

class Swap(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Swap"

    def run(self,game):
        self.participants = game.tribes
        self.record('Drop your buffs!')
        self.reassign_players(game)
        self.wrap_up()
        self.mark_complete()

    def reassign_players(self,game):
        newtribes = cycle(game.tribes)
        shuffle(game.players)
        for player in game.active_players():
            move_to = next(newtribes)
            if move_to == player.tribe:
                verb = 'stays on'
            else:
                verb = 'moves to'
            move_to.add_player(player)
            self.record('{} {} {}.'.format(player.first, verb, move_to))
            # self.result = self.participants

    def wrap_up(self):
        self.record('Let\'s have a look at the new tribes.')
        self.record({x:x.players for x in self.participants})
