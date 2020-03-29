from random import randint, choice, shuffle, normalvariate
from itertools import cycle
from events import generate_schedule
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

        self.tribes = [Tribe() for x in range(tribes)]
        self.players = [Player(next(GENDERS)) for x in range(players)]
        self.assign_players()

        self.schedule = generate_schedule(game=self)

    def assign_players(self, random=True):
        if random:
            shuffle(self.players)
        tr = cycle(self.tribes)
        for player in self.players:
            next(tr).add_player(player)

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
        event = list(filter(lambda x:x.complete == False, self.schedule.events))[0]
        return event

    def next_event(self):
        return self.get_next_event().id

    def run_next(self):
        self.get_next_event().run(self)

class Tribe():
    __tribeId = 0

    def __init__(self,active=True):

        self.id = Tribe.__tribeId
        Tribe.__tribeId += 1
        self.name = choice(NAMES['tribes'])
        self.active = active
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

    def eliminate(self,player):
        self.players.remove(player)
        player.tribe = None



class GameSetupError(Exception):
    pass


game_parameters = {
    'players' : 16,
    'days' : 39,
    'jury' : 7,
    'early_merge' : randint(0,2),
    'final' : 2,
    'tribes' : 2,
}

def check_parameters(par):
    if (par['players']/par['tribes']) % 1 != 0:
        raise GameSetupError('Uneven number of players.')
