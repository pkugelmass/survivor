from random import randint, choice
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def import_names():
    names = {
        'M' : open('male-first-names.txt','r').read().split('\n'),
        'F' : open('female-first-names.txt','r').read().split('\n'),
        'L' : open('last-names.txt','r').read().split('\n')
    }
    return names

NAMES = import_names()

def generate_name(gender):
    first = choice(NAMES[gender]).title()
    last = choice(NAMES['L']).title()
    return (first,last)

class Player():

    def __init__(self,gender):
        self.gender = gender
        self.first, self.last = generate_name(gender)
        self.strategy = randint(1,5)
        self.social = randint(1,5)
        self.physical = randint(1,5)

    def fullname(self):
        return ('{} {}'.format(self.first,self.last))

    def info(self):
        print(self.fullname())
        print(f'Strategy: {self.strategy}')
        print(f'Social: {self.social}')
        print(f'Physical: {self.physical}')

p1 = Player('F')
p1.info()
