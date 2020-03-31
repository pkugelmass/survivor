from random import randint, choice
from .challenges import TribalImmunity, TribalReward, IndividualReward, IndividualImmunity
from .tribal import FinalTribal, TribalCouncil, JuryTribalCouncil
from .special import Merge, Swap

class Schedule:
    def __init__(self):
        self.events = []

    def __str__(self):
        return self.events

    def add_event(self,event):
        self.events.append(event)
        self.sort_events()
        return event

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

def generate_schedule(players=20,days=39,jury=10,final=3, game=None):

    s = Schedule()

    if game:
        players = game.parameters['players']
        days = game.parameters['days']
        jury = game.parameters['jury']
        final = game.parameters['final']
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
    for i,x in enumerate(sorted(tribal_days)):
        if i < players - final - jury:
            tribal = s.add_event(TribalCouncil(x))
        else:
            tribal = s.add_event(JuryTribalCouncil(x))
        tribal.name = '{} #{}'.format(tribal.name,i+1)

    # Merge
    merge_day = s.event_type(JuryTribalCouncil)[0].day-2
    s.add_event(Merge(merge_day))

    # Swap
    swap_day = merge_day - 6
    s.add_event(Swap(swap_day))

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
