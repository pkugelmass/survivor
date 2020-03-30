
class Event():

    eventId = 0

    def __init__(self,day,time=12):

        self.id = Event.eventId
        Event.eventId += 1

        self.day = day
        self.time = time
        self.name = 'Event'
        self.complete = False

        self.num_players = None
        self.num_tribes = None

        self.log = []
        self.participants = None
        self.result = None

    def timestamp(self):
        return self.day + (self.time/100)

    def __repr__(self):
        return '{} - {}'.format(self.timestamp(), self.name)

    def record(self,string):
        self.log.append(string)

    def run(self,game):
        self.mark_complete()
        self.say_goodbye(game)

    def mark_complete(self):
        self.complete = True

    def say_goodbye(self,game):
        pass
