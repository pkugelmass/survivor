from .events import Event
from itertools import cycle

class Merge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Merge"

    def find_participants(self,game):
        self.who = game.tribes

    def start(self):
        self.record('We are merging!')

    def middle(self):
        pass

    def game_changes(self,game):
        [game.retire_tribe(t) for t in game.tribes[::-1]]
        new_name = 'MergedTribe'
        self.record('The new tribe is called {}.'.format(new_name))
        merged_tribe = game.add_tribe(name=new_name)
        [merged_tribe.add_player(x) for x in game.active_players()]
        self.record('Let\'s have a look at the new tribe.')
        self.record({x:x.players for x in self.who})
        self.result = merged_tribe

class Swap(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Swap"

    def find_participants(self,game):
        self.who = game.tribes

    def start(self):
        self.record('Drop your buffs!')

    def middle(self):
        pass

    def game_changes(self,game):
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
        self.record('Let\'s have a look at the new tribes.')
        self.record({x:x.players for x in self.who})
        self.result = self.who

    def end(self):
        pass
