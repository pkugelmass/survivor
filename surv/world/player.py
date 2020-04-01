from random import choice, randint, normalvariate
from surv.utils.names import NAMES, generate_name, generate_hometown


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
        self.alliance = None
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

class Alliance:

    _allianceId = 0

    def __init__(self,players):

        self.id = Alliance._allianceId
        Alliance._allianceId += 1

        self.members = []
        # self.validate(players)
        self.members = [self.add_player(p) for p in players]
        self.active = True
        self.target = None

    def __str__(self):
        return 'Alliance: {}'.format(self.members)

    def __len__(self):
        return len(self.members)

    def link(self):
        return str(self)

    # def validate(self,players=None):
    #     try:
    #         players = self.members
    #     except:
    #         players = players
    #     if not all(isinstance(p,Player) for p in players):
    #         raise AllianceError('Hey, are these all players? {}'.format(players))
    #     if len(players) != len(set(players)):
    #         raise AllianceError('Hey, not all members are unique.')
    #     if len(players) < 2:
    #         raise AllianceError('Alliance of one? {}'.format(players))
    #     return players

    def add_player(self,player):
        if player.alliance != None:
            player.alliance.members.remove(player)
        self.members.append(player)
        player.alliance = self
        return player

    def remove_player(self,player):
        if player not in self.members:
            raise AllianceError('{} not in alliance'.format(player))
        self.members.remove(player)
        player.alliance = None
        if len(self.members) == 1:
            self.remove_player(self.members[0])
            self.active = False


class AllianceError(Exception):
    pass




"""
Ideas for developing players:
* Challenges: Strength, Endurance, Puzzles, Swimming, Dexterity/Steadiness
* Strategy: Anticipation, Decisions, Aggressiveness, Persuasiveness, Loyalty, BS-Detector, Honesty
* Social: Friendliness, Work Ethic, Stability, Leadership
* Factors: Morale, Desire, Hunger, Fatigue, Health
* Others: You're a friend. You're an enemy. You're an ally. You're an opponent. You're a threat. You're a goat.
"""
