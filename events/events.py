
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

    def report_probabilities(self,prob_dict):
        #prob_dict_sorted = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        percentages = ['{}%'.format(round(x,3)*100) for x in prob_dict.values()]
        self.record('Looks like... {}'.format(htmlify(dict(zip(prob_dict.keys(),percentages)))))


def linkify(thing):
    with_links = []
    try:
        if isinstance(thing,dict):
            assert False
        for x in thing:
            if hasattr(x,'link'):
                with_links.append(x.link())
            else:
                with_links.append(x)
        return with_links
    except:
        try:
            for k,v in thing.items():
                if hasattr(k,'link'):
                    with_links.append('{}: {}'.format(k.link(),v))
                else:
                    with_links.append('{}: {}'.format(k.link(),v))
            return with_links
        except:
            if hasattr(thing,'link'):
                return thing.link()
            else:
                return thing

def listify(thing):
    if isinstance(thing, str):
        return thing
    else:
        out = ", ".join(thing[:-1])
        return "{} and {}".format(out, thing[-1])

def htmlify(thing):
    return listify(linkify(thing))
