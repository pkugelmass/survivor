from surv.utils.names import generate_tribe_name

class Tribe():
    __tribeId = 0

    def __init__(self,name=None):

        self.id = Tribe.__tribeId
        Tribe.__tribeId += 1

        if name:
            self.name = name
        else:
            # self.name = choice(NAMES['tribes'])
            self.name = generate_tribe_name()

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

    def link(self):
        return r'<a href="/tribe/{}/">{}</a>'.format(self.id,self.name)

    def __len__(self):
        return len(self.players)
