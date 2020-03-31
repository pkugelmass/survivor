from numpy.random import choice
from itertools import cycle
import re

import os
os.chdir(os.path.dirname(__file__))

def import_names():
    names = {
        'M' : open('data/male-first-names.txt','r').read().split('\n'),
        'F' : open('data/female-first-names.txt','r').read().split('\n'),
        'L' : open('data/last-names.txt','r').read().split('\n'),
        'tribes' : open('data/tribe-names.txt','r').read().split('\n'),
        'jobs' : open('data/occupations.txt','r').read().split('\n'),
        'towns' : open('data/hometowns.txt','r').read().split('\n'),
        'states' : open('data/states.txt','r').read().split('\n')
    }
    names['tribes'] = list(set([x for x in names['tribes'] if len(x)>1]))
    return names

NAMES = import_names()
GENDERS = cycle(['M','F'])

def generate_name(gender):
    first = choice(NAMES[gender]).title()
    last = choice(NAMES['L']).title()
    return (first,last)

def generate_tribe_name():
    names = choice(NAMES['tribes'],size=2)
    justletters = re.sub('\s','',''.join(names))
    syllables = re.findall('[^aeiouAEIOU]+[aeiou]',justletters)
    num_syllables = choice(range(2,len(syllables)))
    new_word = ''.join(choice(syllables,num_syllables,replace=False)).title()
    return new_word

def generate_hometown():
    town = choice(NAMES['towns'])
    state = choice(NAMES['states'])
    return '{}, {}'.format(town,state)
