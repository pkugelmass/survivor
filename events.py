from random import randint,choice,sample,shuffle
from collections import Counter
from itertools import cycle

class Schedule():
    def __init__(self):
        self.events = []

    def __str__(self):
        return self.events

    def add_event(self,event):
        self.events.append(event)
        self.sort_events()

    def sort_events(self):
        self.events = sorted(self.events, key=lambda x: x.timestamp())

    def day(self,day):
        return [x for x in self.events if x.day==day]

    def is_scheduled(self,day,theclass):
        for x in self.day(day):
            if isinstance(x,theclass):
                return True
        return False

    def event_type(self,theclass):
        return [x for x in self.events if isinstance(x,theclass)]

    def tribal_days(self):
        return [x.day for x in self.event_type(TribalCouncil)[:-1]]

    def print_schedule(self):
        for event in self.events:
            print(event)

    def count_type(self,event_type):
        types = [type(x).__name__ for x in s.events]
        matches = len([x for x in types if x == event_type])
        return matches

    def update_num_players(self,players=None,tribes=None):
        last_day = self.events[-1].day
        merge_day = self.event_type(Merge)[0].day
        if players:
            players_per_day = {}
            for day in range(1,last_day+1):
                if self.is_scheduled(day-1,TribalCouncil):
                    players -= 1
                players_per_day[day] = players
            for event in self.events:
                event.num_players = players_per_day[event.day]
                if tribes:
                    if event.day < merge_day:
                        event.num_tribes = tribes
                    else:
                        event.num_tribes = 1

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
        game.day = game.get_next_event().day

    def start(self):
        pass

    def middle(self):
        self.result = choice(self.who)
        self.record('The event selected {}.'.format(self.result))

    def end(self):
        pass

    def game_changes(self,game):
        pass

class Challenge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 12

class IndividualImmunity(Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Immunity'

class IndividualReward(Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Individual Reward'

class TribesMixin:
    def find_participants(self,game):
        self.who = game.tribes

class TribalImmunity(TribesMixin,Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Immunity'

    def start(self):
        for tribe in self.who:
            if tribe.immunity == True:
                self.record('Immunity is back up for grabs.')
                tribe.immunity = False

    def end(self):
        self.record('{} wins immunity!'.format(self.result))
        self.result.immunity = True
        losing_tribes = list(set(self.who) - set([self.result]))
        self.record('{}, I\'ll see you at tribal council.'.format(losing_tribes))

class TribalReward(TribesMixin,Challenge):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Tribal Reward'

    def end(self):
        self.record('{} wins reward!'.format(self.result))
        losing_tribes = list(set(self.who) - set([self.result]))
        self.record('{}, head back to camp; got nothin\' for ya.'.format(losing_tribes))

class Merge(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Merge"

    def find_participants(self,game):
        self.who = game.tribes

    def start(self):
        self.record('We are merging!')

    def middle(self):
        pass

    def game_changes(self,game):
        [game.retire_tribe(t) for t in game.tribes[::-1]]
        new_name = 'MergedTribe'
        self.record('The new tribe is called {}.'.format(new_name))
        merged_tribe = game.add_tribe(name=new_name)
        [merged_tribe.add_player(x) for x in game.active_players()]
        self.record('Let\'s have a look at the new tribe.')
        self.record({x:x.players for x in self.who})
        self.result = merged_tribe

class Swap(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 10
        self.name = "Swap"

    def find_participants(self,game):
        self.who = game.tribes

    def start(self):
        self.record('Drop your buffs!')

    def middle(self):
        pass

    def game_changes(self,game):
        newtribes = cycle(game.tribes)
        shuffle(game.players)
        for player in game.players:
            move_to = next(newtribes)
            if move_to == player.tribe:
                verb = 'stays on'
            else:
                verb = 'moves to'
            move_to.add_player(player)
            self.record('{} {} {}.'.format(player.first, verb, move_to))
        self.record('Let\'s have a look at the new tribes.')
        self.record({x:x.players for x in self.who})
        self.result = self.who

    def end(self):
        pass

class TribalCouncil(Event):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Tribal Council'
        self.votes = {}

    def find_participants(self,game):
        tribe = list(filter(lambda x: x.immunity == False, game.tribes))[0]
        self.who = tribe.players

    def count_votes(self):
        return Counter(self.votes.values())

    def votes_tied(self):
        votes = self.count_votes()
        if len(votes) > 0:
            top2 = votes.most_common(2)
            if top2[0][1] != top2[1][1]:
                return False
        return True

    def start(self):
        self.record('Light your torches...')

    def middle(self):
        while self.votes_tied():
            for player in self.who:
                vote = None
                while vote == None:
                    my_vote = choice(self.who)
                    if my_vote != player and my_vote.immunity == False:
                        vote = my_vote
                self.votes[player] = my_vote

    def end(self):
        cnt = self.count_votes()
        self.record('I\'ll read the votes.')
        self.record(cnt.most_common())
        self.result = cnt.most_common(1)[0][0]
        self.record('Next person voted off Survivor is {}; bring me your torch.'.format(self.result.first))
        self.record('The tribe has spoken. It\'s time for you to go.')
        self.result.eliminated = True
        self.result.tribe.eliminate(self.result)

class JuryTribalCouncil(TribalCouncil):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.time = 19
        self.name = 'Jury Tribal Council'

class FinalTribal(TribalCouncil):
    def __init__(self,day,**kwargs):
        super().__init__(day,**kwargs)
        self.name = 'Final Tribal Council'

def generate_schedule(players=20,days=39,jury=10,final=3, early_merge=randint(0,2), game=None):

    s = Schedule()

    if game:
        players = game.parameters['players']
        days = game.parameters['days']
        jury = game.parameters['jury']
        final = game.parameters['final']
        early_merge = game.parameters['early_merge']
        tribes = game.parameters['tribes']


    # FINAL TRIBAL
    s.add_event(FinalTribal(days))

    # TRIBAL COUNCILS
    tribal_days = []
    num_tribals = players - final
    natural_tribal_days = list(range(3,days-1,3))
    num_natural_tribals = len(natural_tribal_days)
    extra_tribals = []

    if num_tribals > num_natural_tribals:
        still_to_schedule = num_tribals - num_natural_tribals
        day = days-1
        while still_to_schedule > 0:
            if day not in natural_tribal_days:
                extra_tribals.append(day)
                still_to_schedule -= 1
            day -= 1
    elif num_tribals < natural_tribal_days:
        to_remove = num_natural_tribals - num_tribals
        natural_tribal_days = natural_tribal_days[-to_remove]

    tribal_days = natural_tribal_days + extra_tribals
    for i,x in enumerate(tribal_days):
        if i < players - final - jury:
            s.add_event(TribalCouncil(x))
        else:
            s.add_event(JuryTribalCouncil(x))

    # Merge
    merge_day = s.event_type(TribalCouncil)[-jury-2-early_merge].day+1
    s.add_event(Merge(merge_day))

    # Swap
    swap_day = choice([x+1 for x in s.tribal_days()[2:5]])
    if swap_day < merge_day:
        s.add_event(Swap(swap_day))
    #s.add_event(Swap(2))

    # Challenges
    for tribal in s.event_type(TribalCouncil):
        if tribal.day < merge_day:
            s.add_event(TribalImmunity(tribal.day))
            s.add_event(TribalReward(tribal.day-1))
        if tribal.day > merge_day and not s.is_scheduled(tribal.day,FinalTribal):
            s.add_event(IndividualImmunity(tribal.day))
            if s.is_scheduled(tribal.day-1,TribalCouncil) == False:
                s.add_event(IndividualReward(tribal.day-1))

    s.update_num_players(players,tribes)

    return s
