from random import randint, choice, shuffle, normalvariate
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def import_names():
    names = {
        'M' : open('data/male-first-names.txt','r').read().split('\n'),
        'F' : open('data/female-first-names.txt','r').read().split('\n'),
        'L' : open('data/last-names.txt','r').read().split('\n'),
        'tribes' : open('data/tribe-names.txt','r').read().split('\n')
    }
    names['tribes'] = list(set([x for x in names['tribes'] if len(x)>1]))
    return names

NAMES = import_names()

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

        self.strategy = randint(1,5)
        self.social = randint(1,5)
        self.physical = randint(1,5)

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

class Game():
    def __init__(self,tribes=3,players=18):
        self.tribes = [Tribe(x,players/tribes) for x in range(tribes)]
        #self.tribes.append(Tribe('Jury',0,False))

    def active_tribes(self):
        return [tribe for tribe in self.tribes if tribe.active==True]

    def show_tribes(self):
        for tribe in self.active_tribes():
            tribe.show_players()

class Tribe():
    def __init__(self,id,players,active=True):

        self.id = id
        self.name = choice(NAMES['tribes'])
        self.active = active

        players_per_gender = int(players/2)
        self.players = [Player('M') for x in range(players_per_gender)]
        self.players = self.players + [Player('F') for x in range(players_per_gender)]
        # shuffle(self.players)

    def show_players(self):
        print(f'{self.name}: {self.players}')

    def __repr__(self):
        return self.name


class Challenge():
    def __init__(self,tribes):
        self.tribes = tribes
        self.bench = []
        self.equalize_tribes()
        self.strengths = self.calculate_strengths()
        print(f'It\'s a challenge between the tribes {self.tribes}.')
        print(f'Relative strengths are {self.strengths}.')

    def equalize_tribes(self):
        sizes = [len(t.players) for t in self.tribes]
        smallest = min(sizes)
        for t in self.tribes:
            sitout = len(t.players) - smallest
            if sitout > 0:
                print(f'{t} must sit {sitout} player(s) out.')
                for x in range(sitout):
                    p = choice(tribe.players)
                    self.bench.append(p)
                    t.players.remove(p)
                    print(f'{p} takes a seat on the bench.')

    def calculate_strengths(self):
        return [sum([p.physical for p in tribe.players]) for tribe in self.tribes]



# g = Game()
# g.show_tribes()
# c = Challenge(g.tribes)
