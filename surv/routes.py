from flask import render_template, redirect, url_for, request
from surv import app
from .storage import c, new_game, save_game, load_game

@app.route('/')
def home():
    return redirect(url_for('new'))

@app.route('/new/')
def new():
    new_game()
    return redirect(url_for('list'))

@app.route('/list/')
def list():
    return render_template('list.html',title='List',game=load_game())

@app.route('/schedule/')
def schedule():
    return render_template('schedule.html',title="schedule",game=load_game())

@app.route('/event/<eventid>/')
def event(eventid):
    g = load_game()
    this_event = g.get_event(int(eventid))
    return render_template('event.html',title='event',game=g,event=this_event)

@app.route('/run/<eventid>/')
def run(eventid):
    g = load_game()
    this_event = g.get_event(int(eventid))
    if this_event.complete == False:
        this_event.run(g)
        save_game(g)
        return render_template('event.html',title='event',game=g,event=this_event)
    else:
        return redirect(url_for('event',eventid=eventid))

@app.route('/tribe/<tribeid>/')
def tribe(tribeid):
    g = load_game()
    id = int(tribeid)
    this_tribe = [x for x in g.tribes if x.id == id][0]
    return render_template('tribe.html',title='tribe',game=g,tribe=this_tribe)

@app.route('/player/<playerid>/')
def player(playerid):
    id = int(playerid)
    this_player = [x for x in g.players if x.id == id][0]
    return render_template('player.html',title='tribe',game=g,player=this_player)

@app.route('/next/')
def next():
    g = load_game()
    g.run_next()
    save_game(g)
    old_url = request.referrer
    return redirect(old_url)

@app.route('/story/')
def story():
    g = load_game()
    return render_template('story.html',title='Story',game=g)

@app.route('/sim/')
def sim():
    g = load_game()
    g.run_all()
    save_game(g)
    return redirect(url_for('story'))
