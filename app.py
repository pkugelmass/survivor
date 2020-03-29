from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

from main import Game, game_parameters

def reset_game():
    return Game(game_parameters)

g = reset_game()

@app.route('/')
def home():
    return g.tribes[1].name

@app.route('/new/')
def new():
    global g
    g = reset_game()
    return redirect(url_for('list'))

@app.route('/list/')
def list():
    return render_template('list.html',title='List',tribes=g.tribes,game=g)

@app.route('/schedule/')
def schedule():
    return render_template('schedule.html',title="schedule",game=g)

@app.route('/event/<eventid>/')
def event(eventid):
    this_event = g.get_event(int(eventid))
    return render_template('event.html',title='event',game=g,event=this_event)

@app.route('/run/<eventid>/')
def run(eventid):
    this_event = g.get_event(int(eventid))
    this_event.run(g)
    return render_template('event.html',title='event',game=g,event=this_event)
