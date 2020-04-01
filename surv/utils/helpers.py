from numpy.random import choice

def linkify(thing):
    with_links = []
    try:
        if isinstance(thing,(dict,str)):
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
    if isinstance(thing, (str,int)):
        return thing
    else:
        if len(thing) > 1:
            out = ", ".join(thing[:-1])
            return "{} and {}".format(out, thing[-1])
        else:
            return thing[0]

def htmlify(thing):
    return listify(linkify(thing))

def htmlify2(string,*args):
    if len(args) > 0:
        htmlargs = [htmlify(thing) for thing in args]
        string = string.format(*htmlargs)
        return string
    else:
        return htmlify(string)

def player_probabilities(players,func):
    raw_values = [func(p) for p in players]
    norm = [float(v)/sum(raw_values) for v in raw_values]
    prob_dict = dict(zip(players,norm))
    return prob_dict

def player_prob_choice(dict):
    return choice(list(dict.keys()), p=list(dict.values()))

def choose_player(players,func,n=1):
    return player_prob_choice(player_probabilities(players,func))
