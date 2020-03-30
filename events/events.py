from random import randint,choice,sample,shuffle
from itertools import cycle


class Event():

    eventId = 0

    def __init__(self,day,time=12,schedule=None):
        self.id = Event.eventId
        Event.eventId += 1
        self.day = day
        self.time = time
        self.name = 'Event'
        self.complete = False
        self.num_players = None
        self.num_tribes = None
        self.log = []
        self.result = None
        self.who = None

        if schedule:
            schedule.events.append(self)

    def timestamp(self):
        return self.day + (self.time/100)

    def __repr__(self):
        return '{} - {}'.format(self.timestamp(), self.name)

    def record(self,string):
        self.log.append(string)

    def find_participants(self,game):
        self.who = game.players #by default

    def run(self,game):
        self.find_participants(game)
        self.record('{} - {} with {}.'.format(self.name,self.timestamp(),self.who))
        self.start()
        self.middle()
        self.end()
        self.game_changes(game)
        self.complete = True
        try:
            game.day = game.get_next_event().day
        except:
            pass

    def start(self):
        pass

    def middle(self):
        self.result = choice(self.who)
        self.record('The event selected {}.'.format(self.result))

    def end(self):
        pass

    def game_changes(self,game):
        pass
