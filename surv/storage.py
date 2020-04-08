from flask import session
from cachelib.simple import SimpleCache
import pickle
from datetime import datetime

from surv.game.game import Game

c = SimpleCache()

def save_game(game):
    string = pickle.dumps(game)
    c.set(session['id'],string)

def load_game():
    try:
        string = c.get(session['id'])
        game = pickle.loads(string)
        return game
    except:
        return new_game()

def new_game():
    id = str(datetime.now())
    if 'id' in session:
        session.pop('id')
    session['id'] = id
    g = Game()
    save_game(g)
    return g
