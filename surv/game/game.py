from random import shuffle
from itertools import cycle

from surv.game.setup import get_params
from surv.utils.names import GENDERS
from surv.world.player import Player, Alliance
from surv.world.tribe import Tribe
from surv.events.schedule import generate_schedule

class Game():

    __gameid = 0

    def __init__(self,game_parameters=get_params()):

        self.parameters = game_parameters

        players = self.parameters['players']
        tribes = self.parameters['tribes']

        self.id = Game.__gameid
        Game.__gameid += 1

        self.day = 1
        self.gameon = True

        self.tribes = [Tribe() for x in range(tribes)]
        self.old_tribes = []
        self.jury = []
        self.alliances = []

        self.players = [Player(next(GENDERS)) for x in range(players)]

        self.assign_players()

        self.schedule = generate_schedule(game=self)

    def assign_players(self, random=True):
        tr = cycle(self.tribes)
        if random:
            shuffle(self.players)
            for player in self.players:
                next(tr).add_player(player)
        else:
            [next(tr).add_player(x) for x in self.players if x.gender == 'M']
            [next(tr).add_player(x) for x in self.players if x.gender == 'F']

    def active_players(self):
        return [x for x in self.players if not x.eliminated]

    def eliminated_players(self):
        return [x for x in self.players if x.eliminated]

    def add_tribe(self,name=None):
        new_tribe = Tribe(name)
        self.tribes.append(new_tribe)
        return new_tribe

    def retire_tribe(self,tribe):
        if tribe in self.tribes:
            self.old_tribes.append(tribe)
            self.tribes.remove(tribe)

    def eliminate(self,player):
        player.eliminated = True
        player.tribe.players.remove(player)
        player.tribe = None

    def show_tribes(self):
        for tribe in self.active_tribes():
            tribe.show_players()

    def get_event(self,eventId):
        try:
            event = list(filter(lambda x: x.id == eventId, self.schedule.events))[0]
            return event
        except:
            return None

    def get_next_event(self):
        if self.gameon:
            event = list(filter(lambda x:x.complete == False, self.schedule.events))[0]
            return event
        else:
            return self.schedule.events[-1]

    def next_event(self):
        return self.get_next_event().id

    def run_next(self):
        self.get_next_event().run(self)
        self.day = self.get_next_event().day

    def run_all(self):
        while self.gameon:
            self.run_next()

    def create_alliance(self,players):
        a = Alliance(players)
        self.alliances.append(a)
        return a

    def active_alliances(self):
        return [a for a in self.alliances if a.active]
