from random import choice, randint, normalvariate
from surv.game.names import NAMES, generate_name, generate_hometown

class Player():

    __id = 0

    def __init__(self,gender):
        self.id = Player.__id
        Player.__id += 1

        self.gender = gender
        self.first, self.last = generate_name(gender)

        self.age = int(normalvariate(33,8)//1)
        self.job = choice(NAMES['jobs'])
        self.hometown = generate_hometown()

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
        return self.first

    def __repr__(self):
        return self.first

    def link(self):
        return(r'<a href="/player/{}/">{}</a>'.format(self.id,self.first))

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
