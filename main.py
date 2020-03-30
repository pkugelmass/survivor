from random import randint, choice, shuffle, normalvariate
from itertools import cycle
from events.schedule import generate_schedule

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def import_names():
    names = {
        'M' : open('data/male-first-names.txt','r').read().split('\n'),
        'F' : open('data/female-first-names.txt','r').read().split('\n'),
        'L' : open('data/last-names.txt','r').read().split('\n'),
        'tribes' : open('data/tribe-names.txt','r').read().split('\n'),
        'jobs' : open('data/occupations.txt','r').read().split('\n'),
        'towns' : open('data/hometowns.txt','r').read().split('\n')
    }
    names['tribes'] = list(set([x for x in names['tribes'] if len(x)>1]))
    return names

NAMES = import_names()
GENDERS = cycle(['M','F'])

def generate_name(gender):
    first = choice(NAMES[gender]).title()
    last = choice(NAMES['L']).title()
    return (first,last)

game_parameters = {
    'players' : 18,
    'days' : 39,
    'jury' : 10,
    'early_merge' : randint(0,2),
    'final' : 3,
    'tribes' : 2,
}

def check_parameters(par):
    if (par['players']/par['tribes']) % 1 != 0:
        raise GameSetupError('Uneven number of players.')

class Game():

    __gameid = 0

    def __init__(self,game_parameters):

        check_parameters(game_parameters)
        self.parameters = game_parameters

        players = self.parameters['players']
        tribes = self.parameters['tribes']

        self.id = Game.__gameid
        Game.__gameid += 1

        self.day = 1
        self.gameon = True

        self.tribes = [Tribe() for x in range(tribes)]
        self.old_tribes = []

        self.players = [Player(next(GENDERS)) for x in range(players)]
        # self.eliminated = []
        self.jury = []
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

    def add_tribe(self,**kwargs):
        new_tribe = Tribe(**kwargs)
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

    def run_all(self):
        while self.gameon:
            self.run_next()

class Player():

    __id = 0

    def __init__(self,gender):
        self.id = Player.__id
        Player.__id += 1

        self.gender = gender
        self.first, self.last = generate_name(gender)

        self.age = int(normalvariate(33,8)//1)
        self.job = choice(NAMES['jobs'])
        self.hometown = choice(NAMES['towns'])

        self.strategy = randint(1,5)
        self.social = randint(1,5)
        self.physical = randint(1,5)

        self.tribe = None
        self.immunity = False
        self.eliminated = False

    def fullname(self):
        return ('{} {}'.format(self.first,self.last))

    def strength(self):
        return self.strategy + self.social + self.physical

    def __str__(self):
        return self.fullname()

    def __repr__(self):
        return self.first

    def info(self):
        print(self.fullname())
        print(f'ID: {self.id}')
        print(f'Age: {self.age}')
        print(f'Strategy: {self.strategy}')
        print(f'Social: {self.social}')
        print(f'Physical: {self.physical}')
        print(f'Overall: {self.strength()}')

    def move(self,new_tribe):
        new_tribe.add_player(self)

class Tribe():
    __tribeId = 0

    def __init__(self,active=True, name=None):

        self.id = Tribe.__tribeId
        Tribe.__tribeId += 1

        if name:
            self.name = name
        else:
            self.name = choice(NAMES['tribes'])

        self.players = []
        self.immunity = False

    def show_players(self):
        print(f'{self.name}: {self.players}')

    def __repr__(self):
        return self.name

    def add_player(self,player):
        if player.tribe != None:
            player.tribe.players.remove(player)
        self.players.append(player)
        player.tribe = self

class GameSetupError(Exception):
    pass
